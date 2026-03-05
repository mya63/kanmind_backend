from django.urls import path
from authentication.views import registration, login 

urlpatterns = [
    path("registration/", registration),
    path("login/", login),
]