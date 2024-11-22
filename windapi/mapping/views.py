from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import MapDataSources, MapData
from .serializers import MapDataSourcesSerializer, MapDataSerializer


class MapDataSourcesViewSet(viewsets.ModelViewSet):
    """ViewSet for managing MapDataSources."""
    queryset = MapDataSources.objects.all().order_by("id")
    serializer_class = MapDataSourcesSerializer


class MapDataViewSet(viewsets.ModelViewSet):
    """ViewSet for managing MapData."""
    queryset = MapData.objects.all().order_by("id")
    serializer_class = MapDataSerializer
