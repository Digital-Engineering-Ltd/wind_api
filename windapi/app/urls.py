"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Create a simple view function for the homepage
def home(request):
    return HttpResponse("Welcome to the homepage!")

from drf_spectacular.views import (  # type: ignore
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include

# In app/urls.py
from django.urls import path, include
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/user/', include('user.urls')),
    path('api/wind_assessments/', include('wind_assessments.urls')),
    path('api/mapping/', include('mapping.urls')),


    # Add the root path to display a homepage or redirect
    path('', home, name='home'),  # This makes `/` accessible


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

