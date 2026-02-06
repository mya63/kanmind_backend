from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
  health, 
  tasks_list, 
  tasks_detail, 
  tasks_assigned_to_me, 
  tasks_reviewing,)

urlpatterns = [
  path("health/", health),
  path("login/", obtain_auth_token),

  path("tasks/", tasks_list),
  path("tasks/<int:pk>/", tasks_detail),
  
  path("tasks/assigned/", tasks_assigned_to_me),
  path("tasks/assigned-to-me/", tasks_assigned_to_me),

  path("tasks/reviewing/", tasks_reviewing),
]