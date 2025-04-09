import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microservices.settings")
django.setup()

from dotenv import load_dotenv

load_dotenv()