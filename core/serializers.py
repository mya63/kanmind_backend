from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

  """
    Serializer für das Task-Modell.

    Wandelt Task-Objekte in JSON um und validiert
    eingehende JSON-Daten für Create/Update-Requests.
    """

    # Verknüpfung zum User, dem die Aufgabe zugewiesen ist
    # optional, darf leer sein (null)
  assigned_to = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),required=False, allow_null=True
    )
  # Verknüpfung zum Reviewer der Aufgabe
    # ebenfalls optional
  reviewer = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(), required=False, allow_null=True
    )

  class Meta:
    # Das zu serialisierende Modell
    model = Task
    # Alle Felder des Modells werden einbezogen
    fields = "__all__"