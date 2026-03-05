from django.contrib.auth.models import User  
from django.db.models import Q, Count  
from rest_framework import generics, permissions  
from rest_framework.authentication import TokenAuthentication  
from rest_framework.response import Response  
from rest_framework.exceptions import PermissionDenied  

from boards.models import Board  
from boards.serializers import (  
    BoardSerializer,
    BoardListSerializer,
    BoardDetailSerializer,
    BoardPatchSerializer,
)


class BoardListCreateView(generics.ListCreateAPIView):
    """
    List boards for the current user (owner or member) and create new boards.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):  
        return BoardListSerializer if self.request.method == "GET" else BoardSerializer  

    def get_queryset(self):
        """
        Return only boards where the user is owner or member and annotate counts.
        """
        u = self.request.user
        qs = Board.objects.filter(Q(owner=u) | Q(members=u)).distinct()
        return qs.annotate(
            member_count=Count("members", distinct=True),
            ticket_count=Count("tasks", distinct=True),
            tasks_to_do_count=Count("tasks", filter=Q(tasks__status="to-do"), distinct=True),
            tasks_high_prio_count=Count("tasks", filter=Q(tasks__priority="high"), distinct=True),
        )

    def create(self, request, *args, **kwargs):
        """
        Create a board and return the list serializer response (doc-style fields).
        """
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        board = ser.save(owner=request.user)

        # Owner is always a member
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

        return Response(BoardListSerializer(board).data, status=201)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update (PATCH), or delete a board.
    Access is restricted to owner or members.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):  
        if self.request.method == "GET":
            return BoardDetailSerializer
        if self.request.method == "PATCH":
            return BoardPatchSerializer
        return BoardSerializer

    def get_queryset(self):
        """
        Use full queryset so we can return 403 (not 404) for non-members.
        """
        return Board.objects.all().prefetch_related("members", "tasks")

    def get_object(self):
        """
        Enforce board access: only owner or members may access this board.
        """
        obj = super().get_object()
        u = self.request.user
        if obj.owner_id != u.id and not obj.members.filter(id=u.id).exists():
            raise PermissionDenied("Forbidden")
        return obj

    def destroy(self, request, *args, **kwargs):
        """
        Only the board owner may delete the board.
        """
        board = self.get_object()
        if board.owner_id != request.user.id:
            raise PermissionDenied("Only the board owner can delete this board.")
        board.delete()
        return Response(status=204)