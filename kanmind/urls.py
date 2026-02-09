"""
URL configuration for kanmind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

"""
Zentrale URL-Konfiguration des Django-Projekts KanMind.

Hier werden die globalen Routen definiert und
an die jeweiligen Apps weitergeleitet.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  # Django Admin-Oberfläche
    path('admin/', admin.site.urls),
    # Alle API-Endpunkte werden an die core-App delegiert
    # z.B. /api/login/, /api/tasks/, /api/tasks/assigned-to-me/
    path('api/', include('core.urls')),
]
