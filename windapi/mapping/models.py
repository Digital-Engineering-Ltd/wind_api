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

    def __str__(self):
        return f"{self.source.name} - {self.value}"
