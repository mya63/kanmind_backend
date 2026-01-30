from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import health, notes_list, note_detail

urlpatterns = [
  path("health/", health),
  path("notes/", notes_list),
  path("notes/<int:pk>/", note_detail),

  path("login/", obtain_auth_token),
]