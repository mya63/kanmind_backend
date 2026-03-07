from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from boards.models import Board 
from tasks.models import Task, Comment 
from tasks.serializers import TaskSerializer, CommentSerializer  


def _is_board_member(board: Board, user: User) -> bool:
    """Return True if user is the board owner or a board member."""
    if board.owner_id == user.id:
        return True
    return board.members.filter(id=user.id).exists()


def _normalize_task_data(data: dict) -> dict:
    """
    Normalize incoming task data to match the API spec.

     Some tests send 'todo' instead of 'to-do' and 'inprogress' instead of 'in-progress'.
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
    Return a board for the user.

     If no board is provided on task creation:
    - use first board where user is owner
    - else first board where user is member
    - else create a 'Default Board'
    """
    board = Board.objects.filter(owner=user).first()
    if board:
        return board

    board = Board.objects.filter(members=user).first()
    if board:
        return board

    return Board.objects.create(title="Default Board", owner=user)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_list(request):
    """List tasks for boards the user can access, or create a new task."""
    if request.method == "GET":
        qs = Task.objects.filter(board__members=request.user) | Task.objects.filter(board__owner=request.user)
        qs = qs.distinct().order_by("-updated_at")
        return Response(TaskSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    incoming = _normalize_task_data(request.data)
    board_id = incoming.get("board")

    board = get_object_or_404(Board, pk=board_id) if board_id else _get_or_create_default_board(request.user)

    if not _is_board_member(board, request.user):
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    incoming["board"] = board.id

    serializer = TaskSerializer(data=incoming, context={"request": request})
    if serializer.is_valid():
        task = serializer.save(created_by=request.user)  # set created_by server-side
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_detail(request, task_id):
    """Retrieve, update, or delete a task (board access required)."""
    task = get_object_or_404(Task, pk=task_id)

    if request.method in ["GET", "PATCH"] and not _is_board_member(task.board, request.user):
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

    # DELETE allowed only for creator or board owner
    if not (task.created_by_id == request.user.id or task.board.owner_id == request.user.id):
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_assigned_to_me(request):
    """Return tasks assigned to the current user."""
    qs = Task.objects.filter(assignee=request.user).order_by("-updated_at")
    return Response(TaskSerializer(qs, many=True).data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def tasks_reviewing(request):
    """Return tasks where the current user is reviewer."""
    qs = Task.objects.filter(reviewer=request.user).order_by("-updated_at")
    return Response(TaskSerializer(qs, many=True).data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def task_comments(request, task_id):
    """List or create comments for a task (board access required)."""
    task = get_object_or_404(Task, pk=task_id)

    if not _is_board_member(task.board, request.user):
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        qs = Comment.objects.filter(task=task).order_by("created_at")
        return Response(CommentSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    content = request.data.get("content", "")
    if not str(content).strip():
        return Response({"content": "This field may not be blank."}, status=status.HTTP_400_BAD_REQUEST)  # 
    comment = Comment.objects.create(task=task, author=request.user, content=content)
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request, task_id, comment_id):
    """Delete a comment (only the author is allowed)."""
    comment = get_object_or_404(Comment, pk=comment_id, task_id=task_id)

    if comment.author_id != request.user.id:
        return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)