from django.urls import path
from authentication.views import registration, login  # login neu

urlpatterns = [
    path("registration/", registration),
    path("login/", login),
]