from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from wind_assessments.models import RealData, WindMetadata
import pandas as pd

class Command(BaseCommand):
    help = 'Load sample Corine and LiDAR data into the database'

    def handle(self, *args, **kwargs):
        # Sample Corine Data
        corine_data = pd.DataFrame({
            'easting': [123456, 123457],
            'northing': [654321, 654322],
            'roughness': [0.2, 0.25],
        })

        # Sample LiDAR Data
        lidar_data = pd.DataFrame({
            'x': [45.123, 45.124],
            'y': [9.876, 9.877],
            'delta_z': [0.15, 0.18],
        })

        # Create a metadata entry for Corine data
        corine_metadata, _ = WindMetadata.objects.get_or_create(
            station_id="corine_station_1",
            defaults={
                "location": Point(123456, 654321),
                "data_source": "Corine",
            }
        )

        # Load Corine data
        for _, row in corine_data.iterrows():
            RealData.objects.create(
                metadata=corine_metadata,
                dataset_type='corine',
                easting=row['easting'],
                northing=row['northing'],
                roughness_value=row['roughness'],
            )

        self.stdout.write(self.style.SUCCESS("Corine data loaded successfully."))

        # Create a metadata entry for LiDAR data
        lidar_metadata, _ = WindMetadata.objects.get_or_create(
            station_id="lidar_station_1",
            defaults={
                "location": Point(45.123, 9.876),
                "data_source": "LiDAR",
            }
        )

        # Load LiDAR data
        for _, row in lidar_data.iterrows():
            RealData.objects.create(
                metadata=lidar_metadata,
                dataset_type='lidar',
                x=row['x'],
                y=row['y'],
                delta_z=row['delta_z'],
            )

        self.stdout.write(self.style.SUCCESS("LiDAR data loaded successfully."))
