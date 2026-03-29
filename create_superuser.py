# MYA: temporäres Script für Render, um automatisch einen Admin-User anzulegen

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanmind.settings")
django.setup()

from django.contrib.auth.models import User

USERNAME = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
EMAIL = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
PASSWORD = os.getenv("DJANGO_SUPERUSER_PASSWORD", "Admin123456!")

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD,
    )
    print("MYA: Superuser created.")
else:
    print("MYA: Superuser already exists.")