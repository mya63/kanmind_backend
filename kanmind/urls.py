# kanmind/urls.py

from django.contrib import admin
from django.urls import path, include
from authentication.views import EmailCheckView  

urlpatterns = [
    path("admin/", admin.site.urls),

    # Apps
    path("api/", include("authentication.urls")),
    path("api/", include("tasks.urls")),
    path("api/", include("boards.urls")),

    # Extra endpoint
    path("api/email-check/", EmailCheckView.as_view(), name="email-check"),  
]