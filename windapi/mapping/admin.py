from django.contrib import admin

# Register your models here.
from .models import MapDataSources, MapData

# Register MapDataSources with custom display options
class MapDataSourcesAdmin(admin.ModelAdmin):
    list_display = ('name', 'value_description')  # Columns to display in the list view
    search_fields = ('name',)  # Make name searchable in admin
    list_filter = ('name',)  # Filter by name if needed
    ordering = ('name',)  # Order by name by default

admin.site.register(MapDataSources, MapDataSourcesAdmin)


# Register MapData with custom display options
class MapDataAdmin(admin.ModelAdmin):
    list_display = ('source', 'position', 'value', 'date_added')  # Columns to display in the list view
    list_filter = ('source', 'date_added')  # Filter by source and date_added
    search_fields = ('source__name',)  # Make the source's name searchable in admin
    ordering = ('-date_added',)  # Order by date_added in descending order

admin.site.register(MapData, MapDataAdmin)
