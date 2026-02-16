from django.urls import path, include

urlpatterns = [
    path("", include("authentication.urls")),
    path("", include("tasks.urls")),
    path("", include("boards.urls")),
]
