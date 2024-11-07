import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # Ensure 'core' is your project name

application = get_wsgi_application()