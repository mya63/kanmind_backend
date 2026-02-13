from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Board
from .models import Task

from .serializers import TaskSerializer
from .serializers import BoardSerializer

# ---------------------------
# Health-Check Endpoint
# ---------------------------
def health(request):
  # Wird genutzt, um zu prüfen ob das Backend läuft
  return JsonResponse({"status": "ok"})

# ---------------------------
# TASK LIST / CREATE
# ---------------------------

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_list(request):
  # GET: alle Tasks abrufen
  if request.method == "GET":
    tasks = Task.objects.all().order_by("-updated_at")
    return Response(TaskSerializer(tasks, many=True).data)

# POST: neuen Task erstellen
  serializer = TaskSerializer(data=request.data)
  if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  # Fehlerhafte Eingaben
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------
# SINGLE TASK
# ---------------------------

@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_detail(request, pk):
  # Task anhand der ID suchen
  try:
      tasks = Task.objects.get(pk=pk)
  except Task.DoesNotExist:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
  
  # GET: einzelnen Task anzeigen
  if request.method =="GET":
     return Response(TaskSerializer(tasks).data)
  
  # PATCH: Task teilweise aktualisieren
  if request.method =="PATCH":
     serializer = TaskSerializer(tasks, data=request.data, partial=True)
     if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # DELETE: Task löschen
  tasks.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)

  # ---------------------------
# TASKS ASSIGNED TO USER
# ---------------------------
  
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_assigned_to_me(request):
   # Alle Tasks, die dem eingeloggten User zugewiesen sind
   tasks = Task.objects.filter(assigned_to=request.user).order_by("-updated_at")
   return Response(TaskSerializer(tasks, many=True).data)
  
  # ---------------------------
# TASKS USER IS REVIEWING
# ---------------------------
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_reviewing(request):
   tasks = Task.objects.filter(reviewer=request.user).order_by("-updated_at")
   return Response(TaskSerializer(tasks, many=True).data)
  

@api_view(["POST"])
@permission_classes([AllowAny])
def registration (request):
   
   username = request.data.get("username")
   password = request.data.get("password")
   email = request.data.get("email", "")

   if not username or not password:
      return Response({"detail": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)
   
   if User.objects.filter(username=username).exists():
      return Response({"detail": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)
   
   user = User.objects.create_user(username=username, password=password, email=email)
   token, _= Token.objects.get_or_create(user=user)

   return Response({"token": token.key}, status=status.HTTP_201_CREATED)

class BoardListCreateView(generics.ListCreateAPIView):
   authentication_classes = [TokenAuthentication]
   permission_classes = [permissions.IsAuthenticated]
   serializer_class = BoardSerializer

   def get_queryset(self):
      user = self.request.user
      return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
   
   def perform_create(self, serializer):
      board = serializer.save(owner=self.request.user)
      board.members.add(self.request.user)

      member_ids = self.request.data.get("members", [])
      if isinstance(member_ids, list) and member_ids:
         board.members.add(*User.objects.filter(id__in=member_ids))