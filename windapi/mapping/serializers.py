from rest_framework import serializers
from .models import MapDataSources, MapData
from django.contrib.gis import geos as gis_models


class MapDataSourcesSerializer(serializers.ModelSerializer):
    """Serializer for MapDataSources model."""
    class Meta:
        model = MapDataSources
        fields = ['id', 'name', 'value_description']


class MapDataSerializer(serializers.ModelSerializer):
    """Serializer for MapData model."""
    source = serializers.PrimaryKeyRelatedField(queryset=MapDataSources.objects.all())  # Only expect the ID of source
    position = serializers.SerializerMethodField()

    class Meta:
        model = MapData
        fields = ['id', 'position', 'source', 'value', 'date_added', 'x_osgb36', 'y_osgb36', 'type']  # Include the fields

    def get_position(self, obj) -> dict:
        return {
            "type": "Point",
            "coordinates": [obj.position.x, obj.position.y]
        }

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        position_data = data.get('position')
        if position_data:
            if 'coordinates' in position_data:
                internal_value['position'] = gis_models.Point(position_data['coordinates'][0], position_data['coordinates'][1])
            elif isinstance(position_data, list) and len(position_data) == 2:
                internal_value['position'] = gis_models.Point(position_data[0], position_data[1])
        return internal_value
