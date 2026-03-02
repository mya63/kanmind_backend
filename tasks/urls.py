from django.urls import path
from tasks import views

urlpatterns = [
    path("tasks/", views.tasks_list),
    path("tasks/<int:task_id>/", views.tasks_detail),

    path("tasks/assigned-to-me/", views.tasks_assigned_to_me),
    path("tasks/reviewing/", views.tasks_reviewing),

    path("tasks/<int:task_id>/comments/", views.task_comments),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", views.delete_comment),]