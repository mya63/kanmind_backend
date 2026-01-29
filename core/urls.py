from django.urls import path
from .views import health, notes_list, note_detail

urlpatterns = [
  path("health/", health),
  path("notes/", notes_list),
  path("notes/<int:pk>/", note_detail),
]