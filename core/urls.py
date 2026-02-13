from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
  health, 
  tasks_list, 
  tasks_detail, 
  tasks_assigned_to_me, 
  tasks_reviewing,
  registration,
  BoardListCreateView,
  )

urlpatterns = [
  # Health-Check, um zu prüfen ob API läuft
  path("health/", health),

  # Login-Endpunkt
    # Erwartet username + password
    # Gibt Token + Userdaten zurück
  path("login/", obtain_auth_token),

# Alle Tasks anzeigen oder neuen Task erstellen
  path("tasks/", tasks_list),

  # Einzelnen Task abrufen, ändern oder löschen
  path("tasks/<int:pk>/", tasks_detail),
  
  # Tasks, die dem eingeloggten User zugewiesen sind
    # WICHTIG: dieser Pfad wird vom Frontend genutzt
  path("tasks/assigned/", tasks_assigned_to_me),
  path("tasks/assigned-to-me/", tasks_assigned_to_me),

# Tasks, bei denen der User Reviewer ist
  path("tasks/reviewing/", tasks_reviewing),

  path("registration/", registration),

  path('boards/', BoardListCreateView.as_view()),
]