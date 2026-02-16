from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication

from boards.models import Board  # MYA
from boards.serializers import BoardSerializer  # MYA

class BoardListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()  # MYA

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        board.members.add(self.request.user)

        member_ids = self.request.data.get("members", [])
        if isinstance(member_ids, list) and member_ids:
            board.members.add(*User.objects.filter(id__in=member_ids))

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()  # MYA
