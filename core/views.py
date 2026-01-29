from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer

def health(request):
  return JsonResponse({"status": "ok"})


@api_view(["GET"])
def notes_list(request):
  notes = Note.objects.all()
  serializer = NoteSerializer(notes, many=True)
  return Response(serializer.data)