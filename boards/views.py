from django.contrib.auth.models import User
from django.db.models import Q, Count  # MYA
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response  # MYA
from rest_framework.exceptions import PermissionDenied  # MYA

from boards.models import Board  # MYA
from boards.serializers import (
    BoardSerializer,         # MYA
    BoardListSerializer,     # MYA
    BoardDetailSerializer,
    BoardPatchSerializer   # MYA
)


class BoardListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):  # MYA
        return BoardListSerializer if self.request.method == "GET" else BoardSerializer  # MYA

    def get_queryset(self):
        u = self.request.user
        qs = Board.objects.filter(Q(owner=u) | Q(members=u)).distinct()  # MYA
        return qs.annotate(  # MYA: Counts wie Doku
            member_count=Count("members", distinct=True),
            ticket_count=Count("tasks", distinct=True),
            tasks_to_do_count=Count("tasks", filter=Q(tasks__status="to-do"), distinct=True),
            tasks_high_prio_count=Count("tasks", filter=Q(tasks__priority="high"), distinct=True),
        )

    def create(self, request, *args, **kwargs):  # MYA: POST Response doku-konform
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        board = ser.save(owner=request.user)

        board.members.add(request.user)
        mids = request.data.get("members", [])
        if isinstance(mids, list) and mids:
            board.members.add(*User.objects.filter(id__in=mids))

        board = Board.objects.filter(id=board.id).annotate(
            member_count=Count("members", distinct=True),
            ticket_count=Count("tasks", distinct=True),
            tasks_to_do_count=Count("tasks", filter=Q(tasks__status="to-do"), distinct=True),
            tasks_high_prio_count=Count("tasks", filter=Q(tasks__priority="high"), distinct=True),
        ).first()

        return Response(BoardListSerializer(board).data, status=201)  # MYA


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):  # MYA
        if self.request.method == "GET":
            return BoardDetailSerializer  # MYA
        if self.request.method == "PATCH":
            return BoardPatchSerializer  # MYA: Doku PATCH Response
        return BoardSerializer  # MYA (z.B. DELETE egal)
    
    def get_queryset(self):  # MYA: nicht filtern -> 403 möglich
        return Board.objects.all().prefetch_related("members", "tasks")  # MYA

    def get_object(self):  # MYA: 403 wenn kein Zugriff
        obj = super().get_object()
        u = self.request.user
        if obj.owner_id != u.id and not obj.members.filter(id=u.id).exists():
            raise PermissionDenied("Forbidden")  # MYA
        return obj
    def destroy(self, request, *args, **kwargs):
        board = self.get_object()

    # Only owner is allowed to delete the board
        if board.owner_id != request.user.id:
            raise PermissionDenied("Only the board owner can delete this board.")

        board.delete()
        return Response(status=204)