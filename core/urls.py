from django.urls import path
from .views import health, notes_list

urlpatterns = [
  path("health/", health),
  path("notes/", notes_list),
]