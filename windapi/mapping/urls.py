from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MapDataSourcesViewSet, MapDataViewSet

router = DefaultRouter()
router.register(r'sources', MapDataSourcesViewSet)  # Endpoint: /api/mapping/sources/
router.register(r'data', MapDataViewSet)           # Endpoint: /api/mapping/data/

urlpatterns = [
    path('', include(router.urls)),
]
