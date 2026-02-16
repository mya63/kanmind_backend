from django.urls import path
from boards.views import BoardListCreateView, BoardDetailView  # MYA

urlpatterns = [
    path("boards/", BoardListCreateView.as_view()),
    path("boards/<int:pk>/", BoardDetailView.as_view()),
]
