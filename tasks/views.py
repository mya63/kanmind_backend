# tasks/views.py

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from boards.models import Board  # MYA
from tasks.models import Task, Comment  # MYA
from tasks.serializers import TaskSerializer, CommentSerializer  # MYA


def _is_board_member(board: Board, user: User) -> bool:
    # MYA: Owner zählt als Member
    if board.owner_id == user.id:
        return True
    return board.members.filter(id=user.id).exists()


def _normalize_task_data(data: dict) -> dict:
    """
    MYA: Tests schicken teils 'todo' statt 'to-do' -> mappen.
    """
    d = dict(data)
    status_val = d.get("status")

    if status_val == "todo":
        d["status"] = "to-do"
    elif status_val == "inprogress":
        d["status"] = "in-progress"

    return d


def _get_or_create_default_board(user: User) -> Board:
    """
    MYA: Wenn kein board im POST kommt:
    - nimm erstes Board wo User Owner ist
    - sonst erstes Board wo User Member ist
    - sonst erstelle Default-Board
    """
    board = Board.objects.filter(owner=user).first()
    if board:
        return board

    board = Board.objects.filter(members=user).first()
    if board:
        return board

    # MYA: Fix für Tests -> Default Board erzeugen
    return Board.objects.create(title="Default Board", owner=user)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_list(request):
    if request.method == "GET":
        qs = Task.objects.filter(board__members=request.user) | Task.objects.filter(board__owner=request.user)
        qs = qs.distinct().order_by("-updated_at")
        return Response(TaskSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    # ------------------------
    # POST
    # ------------------------
    incoming = _normalize_task_data(request.data)
    board_id = incoming.get("board")

    if board_id:
        board = get_object_or_404(Board, pk=board_id)
    else:
        board = _get_or_create_default_board(request.user)

    if not _is_board_member(board, request.user):
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    incoming["board"] = board.id

    serializer = TaskSerializer(data=incoming, context={"request": request})
    if serializer.is_valid():
        task = serializer.save(created_by=request.user)  # MYA: created_by serverseitig
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method in ["GET", "PATCH"]:
        if not _is_board_member(task.board, request.user):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        incoming = _normalize_task_data(request.data)
        serializer = TaskSerializer(task, data=incoming, partial=True, context={"request": request})
        if serializer.is_valid():
            updated = serializer.save()
            return Response(TaskSerializer(updated).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: nur Task-Ersteller oder Board-Owner
    if not (task.created_by_id == request.user.id or task.board.owner_id == request.user.id):
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_assigned_to_me(request):
    qs = Task.objects.filter(assignee=request.user).order_by("-updated_at")
    return Response(TaskSerializer(qs, many=True).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_reviewing(request):
    qs = Task.objects.filter(reviewer=request.user).order_by("-updated_at")
    return Response(TaskSerializer(qs, many=True).data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_comments(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if not _is_board_member(task.board, request.user):
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        qs = Comment.objects.filter(task=task).order_by("created_at")
        return Response(CommentSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    content = request.data.get("content", "")
    if not str(content).strip():
        return Response({"content": "Dieser Wert darf nicht leer sein."}, status=status.HTTP_400_BAD_REQUEST)

    comment = Comment.objects.create(task=task, author=request.user, content=content)
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request, task_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, task_id=task_id)

    # 🔥 ABSOLUT KEIN Board-Check hier!
    # Nur der Author darf löschen
    if comment.author_id != request.user.id:
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)