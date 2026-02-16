from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from tasks.models import Task  # MYA
from tasks.serializers import TaskSerializer  # MYA

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_list(request):
    if request.method == "GET":
        qs = Task.objects.all().order_by("-updated_at")
        return Response(TaskSerializer(qs, many=True).data)

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(TaskSerializer(task).data)

    if request.method == "PATCH":
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_assigned_to_me(request):
    qs = Task.objects.filter(assigned_to=request.user).order_by("-updated_at")
    return Response(TaskSerializer(qs, many=True).data)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_reviewing(request):
    qs = Task.objects.filter(reviewer=request.user).order_by("-updated_at")
    return Response(TaskSerializer(qs, many=True).data)
