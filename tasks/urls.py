from django.urls import path
from tasks.views import tasks_list, tasks_detail, tasks_assigned_to_me, tasks_reviewing  # MYA

urlpatterns = [
    path("tasks/", tasks_list),
    path("tasks/<int:pk>/", tasks_detail),
    path("tasks/assigned-to-me/", tasks_assigned_to_me),
    path("tasks/reviewing/", tasks_reviewing),
]
