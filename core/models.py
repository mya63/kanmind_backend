from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

  """
    Datenbankmodell für eine Aufgabe (Task).

    Repräsentiert eine einzelne Aufgabe im KanMind-System,
    inklusive Status, Zuweisung und Zeitstempel.
    """

    # Mögliche Status-Werte einer Aufgabe

  STATUS_CHOICES = [
    ("todo", "To Do"),
    ("in_progress", "In Progress"),
    ("done", "Done"),
  ]


# Titel der Aufgabe (Pflichtfeld)
  title = models.CharField(max_length=255)

   # Beschreibung der Aufgabe (optional)
  description = models.TextField(blank=True)

  # Aktueller Status der Aufgabe
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")

# Benutzer, dem die Aufgabe zugewiesen ist
    # Wird der User gelöscht, bleibt die Aufgabe bestehen
  assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")

# Benutzer, der die Aufgabe überprüft
  reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_tasks")

# Erstellungszeitpunkt der Aufgabe
  created_at = models.DateTimeField(auto_now_add=True)

  # Zeitpunkt der letzten Änderung
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      # Anzeige der Aufgabe im Django-Admin
      return self.title
