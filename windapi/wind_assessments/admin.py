from django.contrib import admin

# # Register your models here.
# from .models import WindMetadata, RealData  # Import your models

# # Register WindMetadata model
# @admin.register(WindMetadata)
# class WindMetadataAdmin(admin.ModelAdmin):
#     list_display = ('station_id', 'data_source', 'location')  # Fields to display in the list view
#     search_fields = ('station_id', 'data_source')  # Fields to search by in the admin

# # Register RealData model
# @admin.register(RealData)
# class RealDataAdmin(admin.ModelAdmin):
#     list_display = ('dataset_type', 'metadata', 'easting', 'northing', 'roughness_value', 'x', 'y', 'delta_z')  # Customize what fields to display
#     search_fields = ('dataset_type', 'metadata__station_id')  # Add searchable fields
#     list_filter = ('dataset_type',)  # Add filtering options
