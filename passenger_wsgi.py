import sys
import os

# Add your project directory to the sys.path
sys.path.insert(0, '/home/goontrav/public_html/Travel_Core')

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Travel_Core.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()