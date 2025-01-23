from django.db import models
# Create your models here.
from django.contrib.gis.db import models as gis_models

class MapDataSources(models.Model):
    """Model to store metadata for map data sources."""
    name = models.CharField(max_length=255)
    value_description = models.TextField()

    def __str__(self):
        return self.name


class MapData(models.Model):
    """Model to store map data."""
    position = gis_models.PointField()
    source = models.ForeignKey(MapDataSources, on_delete=models.CASCADE, related_name="map_data")
    value = models.FloatField()
    date_added = models.DateField(auto_now_add=True)
    x_osgb36 = models.FloatField(null=True, blank=True)  # Add this field
    y_osgb36 = models.FloatField(null=True, blank=True)  # Add this field
    type = models.CharField(max_length=50, null=True, blank=True)  # Add this field

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['position', 'source', 'value'], name='unique_position_source_value')
        ]

    def __str__(self):
        return f"{self.source.name} - {self.value}"
