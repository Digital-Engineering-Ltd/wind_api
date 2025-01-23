from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import MapDataSources, MapData


# @admin.register(MapDataSources)
# class MapDataSourcesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'value_description')

# @admin.register(MapData)
# class MapDataAdmin(admin.ModelAdmin):
#     list_display = ('id', 'position', 'source', 'value', 'date_added', 'map')
#     search_fields = ('source__name',)
#     list_filter = ('source', 'date_added')


# Register your models here
@admin.register(MapDataSources)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value_description')  # Customize columns
    search_fields = ('name',)

@admin.register(MapData)
class MapDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'value', 'source', 'date_added')  # Customize columns
    search_fields = ('source__name',)
    list_filter = ('date_added',)



    def map(self, obj):
        return mark_safe(f'<div id="map_{obj.id}" style="width: 100%; height: 400px;"></div>'
                         f'<script>'
                         f'var map = L.map("map_{obj.id}").setView([{obj.position.y}, {obj.position.x}], 13);'
                         f'L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{'
                         f'    maxZoom: 19'
                         f'}}).addTo(map);'
                         f'L.marker([{obj.position.y}, {obj.position.x}]).addTo(map);'
                         f'</script>')

    map.short_description = 'Map'
    map.allow_tags = True
