from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import MapDataSources, MapData


class MapDataSourcesSerializer(serializers.ModelSerializer):
    """Serializer for MapDataSources model."""
    class Meta:
        model = MapDataSources
        fields = ['id', 'name', 'value_description']


class MapDataSerializer(GeoFeatureModelSerializer):
    """Serializer for MapData model."""
    source = MapDataSourcesSerializer()  # Optionally serialize the related source

    class Meta:
        model = MapData
        geo_field = 'position'
        fields = ['id', 'position', 'source', 'value', 'date_added']
