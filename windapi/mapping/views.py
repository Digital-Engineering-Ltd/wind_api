from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from django.http import HttpResponse
from .models import MapDataSources, MapData
from .serializers import MapDataSourcesSerializer, MapDataSerializer
from .filters import MapDataFilter
import logging
from pyproj import Transformer

logger = logging.getLogger(__name__)

# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView


class MapDataSourcesViewSet(viewsets.ModelViewSet):
    """ViewSet for managing MapDataSources."""
    queryset = MapDataSources.objects.all().order_by("id")
    serializer_class = MapDataSourcesSerializer


class MapDataViewSet(viewsets.ModelViewSet):
    """ViewSet for managing MapData."""
    queryset = MapData.objects.all().order_by("id")
    serializer_class = MapDataSerializer


class ExportMapDataView(GenericAPIView):
    """Export filtered map data as CSV."""
    queryset = MapData.objects.all()
    serializer_class = MapDataSerializer
    filterset_class = MapDataFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        logger.info(f"Filtered queryset count: {queryset.count()}")

        data = self.get_serializer(queryset, many=True).data

        # Initialize the transformer for coordinate transformation
        transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326")  # OSGB36 to WGS84

        # Replace 'source' field with the related MapDataSources model name and perform transformations
        for item in data:
            item['source'] = MapDataSources.objects.get(id=item['source']).name
            item['x'] = item['position']['coordinates'][0]
            item['y'] = item['position']['coordinates'][1]
            item['x_osgb36'], item['y_osgb36'] = transformer.transform(item['x'], item['y'])
            item['roughness'] = item['value']
            item['type'] = item['source']  # Assuming 'source' field indicates the type (LiDAR or Corine)

        # Select only the required fields for the CSV
        df = pd.DataFrame(data, columns=['x', 'y', 'x_osgb36', 'y_osgb36', 'roughness', 'type'])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="map_data.csv"'
        df.to_csv(path_or_buf=response, index=False)

        return response
