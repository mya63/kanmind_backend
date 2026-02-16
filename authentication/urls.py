from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from authentication.views import registration

urlpatterns = [
    path("login/", obtain_auth_token),
    path("registration/", registration),
]
