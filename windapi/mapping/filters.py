from django_filters import rest_framework as filters
from .models import MapData

class MapDataFilter(filters.FilterSet):
    """Filter for MapData."""
    bbox = filters.CharFilter(method='filter_bbox')
    start_date = filters.DateFilter(field_name='date_added', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date_added', lookup_expr='lte')
    source = filters.CharFilter(field_name='source__name', lookup_expr='icontains')

    class Meta:
        model = MapData
        fields = ['bbox', 'start_date', 'end_date', 'source']

    def filter_bbox(self, queryset, name, value):
        try:
            min_x, min_y, max_x, max_y = map(float, value.split(','))
            return queryset.filter(position__within=(
                (min_x, min_y),
                (max_x, max_y)
            ))
        except ValueError:
            return queryset.none()
