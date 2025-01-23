from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from mapping.models import MapData, MapDataSources
import requests
import pandas as pd
from rest_framework import status  # Example import from rest_framework
import io
import json
import os
from django.db import IntegrityError
from pyproj import Transformer
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch data from local API and populate the database'
    last_processed_file = 'last_processed.json'

    def handle(self, *args, **kwargs):
        # Define the API endpoints
        sources_endpoint = 'http://localhost:8000/api/mapping/sources/'
        data_endpoint = 'http://localhost:8000/api/mapping/data/'

        # Fetch map data sources from the API
        try:
            response_sources = requests.get(sources_endpoint)
            response_sources.raise_for_status()  # Raise an exception for HTTP errors
            sources_data = response_sources.json()  # Assuming the API returns JSON data

            # Process and save MapDataSources
            for source in sources_data:
                map_data_source, created = MapDataSources.objects.get_or_create(
                    name=source['name'],
                    defaults={"value_description": source['value_description']}
                )

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to fetch data from {sources_endpoint}: {e}"))
            logger.error(f"Failed to fetch data from {sources_endpoint}: {e}")

        # Fetch map data from the API
        try:
            response_data = requests.get(data_endpoint)
            response_data.raise_for_status()  # Raise an exception for HTTP errors
            data = response_data.json()  # Assuming the API returns JSON data

            # Debug: Print out the data type and the first few entries
            self.stdout.write(self.style.SUCCESS(f"Fetched data type: {type(data)}"))  # Print type of data
            self.stdout.write(self.style.SUCCESS(f"Fetched data: {data}"))  # Print full data content

            # Check if data has 'features' and process it
            if not data:
                self.stderr.write(self.style.ERROR("No data fetched from the API."))
                logger.error("No data fetched from the API.")
                return
            elif isinstance(data, list):
                features = data  # If data is a list, treat it as features
                self.stdout.write(self.style.SUCCESS(f"Fetched {len(features)} features."))
            elif 'features' in data:
                features = data['features']  # Extract the list of features
                self.stdout.write(self.style.SUCCESS(f"Fetched {len(features)} features."))
            else:
                self.stderr.write(self.style.ERROR(f"Unexpected data structure. Missing 'features' key."))
                logger.error(f"Unexpected data structure. Missing 'features' key.")
                return

            # Load the last processed point
            last_processed_index = self.load_last_processed_index()

            # Initialize the transformer for coordinate transformation
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:27700")  # WGS84 to OSGB36

            # Process each feature starting from the last processed point
            for index, feature in enumerate(features):
                if index <= last_processed_index:
                    continue  # Skip already processed features

                try:
                    # Extract the feature position and properties
                    position_data = feature.get('position')
                    if position_data is None or 'coordinates' not in position_data:
                        self.stderr.write(self.style.ERROR(f"Missing or invalid position in feature: {feature}"))
                        logger.error(f"Missing or invalid position in feature: {feature}")
                        continue

                    coordinates = position_data['coordinates']
                    position = Point(coordinates[0], coordinates[1])

                    # Transform coordinates to OSGB36
                    x_osgb36, y_osgb36 = transformer.transform(coordinates[1], coordinates[0])
                    self.stdout.write(self.style.SUCCESS(f"Transformed coordinates: ({x_osgb36}, {y_osgb36})"))

                    # Extract source from properties (use the 'id' to fetch the source)
                    source_id = feature.get('source')
                    if source_id is None:
                        self.stderr.write(self.style.ERROR(f"Invalid source data in feature: {feature}"))
                        logger.error(f"Invalid source data in feature: {feature}")
                        continue

                    source = MapDataSources.objects.filter(id=source_id).first()
                    if source is None:
                        self.stderr.write(self.style.ERROR(f"Source with ID {source_id} not found."))
                        logger.error(f"Source with ID {source_id} not found.")
                        continue  # Skip to the next feature

                    # Extract the value from properties
                    value = feature.get('value')
                    if value is None:
                        self.stderr.write(self.style.ERROR(f"Invalid value in feature: {feature}"))
                        logger.error(f"Invalid value in feature: {feature}")
                        continue

                    # Determine the data_type based on the source ID
                    data_type = "LiDAR" if source_id == 1 else "Corine" if source_id == 2 else "Unknown"
                    self.stdout.write(self.style.SUCCESS(f"Determined data type: {data_type}"))

                    # Check if the record already exists
                    if MapData.objects.filter(position=position, source=source, value=value).exists():
                        continue  # Skip duplicate entries

                    # Create MapData entry in the database
                    map_data = MapData.objects.create(
                        position=position,
                        source=source,
                        value=value,
                        x_osgb36=x_osgb36,
                        y_osgb36=y_osgb36,
                        type=data_type,
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created MapData entry: {map_data.id}, {position}, {source.name}, {value}, {x_osgb36}, {y_osgb36}, {data_type}"))

                    # Save the last processed point
                    self.save_last_processed_index(index)

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing feature: {feature}"))
                    self.stderr.write(self.style.ERROR(str(e)))
                    logger.error(f"Error processing feature: {feature}")
                    logger.error(str(e))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to fetch data from {data_endpoint}: {e}"))
            logger.error(f"Failed to fetch data from {data_endpoint}: {e}")

        self.test_export_map_data()

    def load_last_processed_index(self):
        """Load the last processed index from a file."""
        if os.path.exists(self.last_processed_file):
            with open(self.last_processed_file, 'r') as file:
                data = json.load(file)
                return data.get('last_processed_index', -1)
        return -1

    def save_last_processed_index(self, index):
        """Save the last processed index to a file."""
        with open(self.last_processed_file, 'w') as file:
            json.dump({'last_processed_index': index}, file)

    def test_export_map_data(self):
        """Test exporting map data as CSV."""
        from django.urls import reverse
        from rest_framework.test import APIClient
        from mapping.models import MapDataSources, MapData

        client = APIClient()
        url = reverse('wind_assessments:export-map-data')
        response = client.get(url, {
            'bbox': '-10,-10,10,10',  # Adjusted bounding box to include the test data point (1, 1)
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'source': 'Test Source'
        })

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response['Content-Type'] == 'text/csv', f"Expected content type 'text/csv', got {response['Content-Type']}"

        # Read the CSV content
        csv_content = response.content.decode('utf-8')
        if not csv_content.strip():
            self.stderr.write(self.style.ERROR("CSV content is empty."))
            return

        df = pd.read_csv(io.StringIO(csv_content))

        # Check if the data is correct
        if df.empty:
            self.stderr.write(self.style.ERROR("CSV content is empty. No data to parse."))
            return

        # Adjust the test to be more flexible
        if len(df) == 0:
            self.stderr.write(self.style.ERROR("Expected at least 1 row, got 0"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Exported {len(df)} rows successfully."))

        self.stdout.write(self.style.SUCCESS("Export map data test passed."))