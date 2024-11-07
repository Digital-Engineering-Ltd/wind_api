"""
Database models for Wind Assessments.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.utils import timezone

# Create your models here.


class Turbine(models.Model):
    """Model to represent a Turbine."""
    name = models.CharField(max_length=255)
    capacity = models.DecimalField(
        max_digits=6,
        decimal_places=2)  # Capacity in MW (e.g., 3.5 MW)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.capacity} MW)"


class WindAssessment(models.Model):
    REPORT_TYPE_CHOICES = [
        ('feasibility', 'Feasibility Assessment'),
        ('wind_resource', 'Wind Resource Assessment'),
        ('site_suitability', 'Site Suitability Assessment'),
    ]

    TURBINE_CHOICES = [
        ('turbine_model_a', 'Turbine Model A'),
        ('turbine_model_b', 'Turbine Model B'),
    ]

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    customer_name = models.CharField(max_length=255)
    site_name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    lat = models.DecimalField(max_digits=8, decimal_places=5, default=0.0)
    lon = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        default=0.0)
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True)
    turbine_type = models.CharField(
        max_length=20,
        choices=TURBINE_CHOICES)  # This is correct
    date = models.DateField()
    assessment_notes = models.TextField(null=True, blank=True)
    report_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Wind Assessment for {self.customer_name}"








class WindMetadata(models.Model):
    """
    Model to store metadata related to wind data collection,
    including location and site-specific details.
    """

    # Unique station identifier and description fields
    station_id = models.CharField(max_length=50, unique=True, help_text="Unique ID for the data collection station")
    location = models.PointField(geography=True, help_text="Location of the station as latitude and longitude")
    elevation = models.FloatField(null=True, blank=True, help_text="Elevation above sea level in meters")
    data_source = models.CharField(max_length=100, help_text="Source of the data, e.g., NOAA")
    frequency = models.CharField(max_length=20, help_text="Frequency of data collection, e.g., hourly, daily")
    data_units = models.CharField(max_length=50, help_text="Units of measurement, e.g., m/s for wind speed")
    date_collected = models.DateTimeField(default=timezone.now, help_text="Date and time when metadata was recorded")
    description = models.TextField(blank=True, help_text="Additional description of the dataset")

    class Meta:
        verbose_name_plural = "Wind Metadata"

    def __str__(self):
        return f"Metadata for station {self.station_id} at {self.location}"







class RealData(models.Model):
    """
    Model to store both Corine and LiDAR wind assessment data.
    """

    DATASET_TYPE_CHOICES = [
        ('corine', 'Corine'),
        ('lidar', 'LiDAR'),
    ]

    dataset_type = models.CharField(
        max_length=20,
        choices=DATASET_TYPE_CHOICES,
        default='corine',  # Ensure a sensible default value
        help_text="Type of dataset (Corine or LiDAR)"
    )

    # Link to the related metadata for context
    metadata = models.ForeignKey(WindMetadata, on_delete=models.CASCADE, related_name="real_data")

    # Corine-specific fields
    easting = models.FloatField(null=True, blank=True, help_text="Easting coordinate for Corine data")
    northing = models.FloatField(null=True, blank=True, help_text="Northing coordinate for Corine data")
    roughness_value = models.FloatField(null=True, blank=True, help_text="Roughness value for Corine data")

    # LiDAR-specific fields
    x = models.FloatField(null=True, blank=True, help_text="X coordinate for LiDAR data")
    y = models.FloatField(null=True, blank=True, help_text="Y coordinate for LiDAR data")
    delta_z = models.FloatField(null=True, blank=True, help_text="Delta Z (roughness) value for LiDAR data")

    # Shared timestamp
    #timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of data collection")

    class Meta:
        verbose_name_plural = "Real Data"

    def __str__(self):
        return f"{self.dataset_type} data at ({self.easting or self.x}, {self.northing or self.y}) - Roughness: {self.roughness_value or self.delta_z}"

