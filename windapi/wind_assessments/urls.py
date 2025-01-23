"""
URL mappings for the Wind Assessment API.
"""
from django.urls import path
from wind_assessments import views
from mapping.views import ExportMapDataView  # Update the import

app_name = 'wind_assessments'

urlpatterns = [
    path(
        'wind_assessment/create/',
        views.CreateWindAssessmentView.as_view(),
        name='create-wind-assessment'),
    path(
        'wind_assessment/',
        views.ListWindAssessmentView.as_view(),
        name='list-wind-assessment'),
    path(
        'wind_assessment/<int:pk>/',
        views.RetrieveUpdateWindAssessmentView.as_view(),
        name='detail-wind-assessment'),
    path('export_map_data/', ExportMapDataView.as_view(), name='export-map-data'),  # Update the view
]
