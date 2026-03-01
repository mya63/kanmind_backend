from django.urls import path, include
from authentication.views import EmailCheckView


urlpatterns = [
    path("", include("authentication.urls")),
    path("", include("tasks.urls")),
    path("", include("boards.urls")),
    path("email-check/", EmailCheckView.as_view(), name="email-check"),

]
