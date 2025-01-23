# from django.core.management.base import BaseCommand
# from django.contrib.gis.geos import Point
# from wind_assessments.models import RealData, WindMetadata
# import pandas as pd

# class Command(BaseCommand):
#     help = 'Load sample Corine and LiDAR data into the database'

#     def handle(self, *args, **kwargs):
#         # Sample Corine Data
#         corine_data = pd.DataFrame({
#             'easting': [123456, 123457],
#             'northing': [654321, 654322],
#             'roughness': [0.2, 0.25],
#         })

#         # Sample LiDAR Data
#         lidar_data = pd.DataFrame({
#             'x': [45.123, 45.124],
#             'y': [9.876, 9.877],
#             'delta_z': [0.15, 0.18],
#         })

#         # Create a metadata entry for Corine data
#         corine_metadata, _ = WindMetadata.objects.get_or_create(
#             station_id="corine_station_1",
#             defaults={
#                 "location": Point(123456, 654321),
#                 "data_source": "Corine",
#             }
#         )

#         # Load Corine data
#         for _, row in corine_data.iterrows():
#             RealData.objects.create(
#                 metadata=corine_metadata,
#                 dataset_type='corine',
#                 easting=row['easting'],
#                 northing=row['northing'],
#                 roughness_value=row['roughness'],
#             )

#         self.stdout.write(self.style.SUCCESS("Corine data loaded successfully."))

#         # Create a metadata entry for LiDAR data
#         lidar_metadata, _ = WindMetadata.objects.get_or_create(
#             station_id="lidar_station_1",
#             defaults={
#                 "location": Point(45.123, 9.876),
#                 "data_source": "LiDAR",
#             }
#         )

#         # Load LiDAR data
#         for _, row in lidar_data.iterrows():
#             RealData.objects.create(
#                 metadata=lidar_metadata,
#                 dataset_type='lidar',
#                 x=row['x'],
#                 y=row['y'],
#                 delta_z=row['delta_z'],
#             )

#         self.stdout.write(self.style.SUCCESS("LiDAR data loaded successfully."))





#use the one below

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point  # For creating PointField values
from mapping.models import MapData, MapDataSources
import pandas as pd

class Command(BaseCommand):
    help = 'Load sample data for MapData and MapDataSources'

    def handle(self, *args, **kwargs):
        # Sample map data sources (for example, different map providers)
        map_data_sources = [
            {"name": "Corine Data", "value_description": "Corine land cover data"},
            {"name": "LiDAR Data", "value_description": "LiDAR-based elevation data"},
        ]

        # Load map data sources into the database
        for data_source in map_data_sources:
            MapDataSources.objects.get_or_create(
                name=data_source['name'],
                value_description=data_source['value_description']
            )

        self.stdout.write(self.style.SUCCESS("MapDataSources loaded successfully."))

        # Sample map data (positions as tuples of (longitude, latitude), value as height or roughness)
        map_data = [
            {"position": (45.123, 9.876), "source_name": "Corine Data", "value": 10.5},
            {"position": (45.124, 9.877), "source_name": "Corine Data", "value": 12.3},
            {"position": (45.125, 9.878), "source_name": "LiDAR Data", "value": 15.7},
            {"position": (45.126, 9.879), "source_name": "LiDAR Data", "value": 14.2},
        ]

        # Iterate over the map data and create MapData records
        for data in map_data:
            # Get the corresponding MapDataSource object based on the source_name
            source = MapDataSources.objects.get(name=data['source_name'])

            # Create a Point object for the position field
            position = Point(data['position'][0], data['position'][1])

            # Create the MapData record
            MapData.objects.create(
                position=position,
                source=source,
                value=data['value'],
            )

        self.stdout.write(self.style.SUCCESS("MapData loaded successfully."))
