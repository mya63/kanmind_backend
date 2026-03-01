from django.contrib.auth.models import User  # MYA
from rest_framework import serializers
from boards.models import Board  # MYA


class BoardListSerializer(serializers.ModelSerializer):  # MYA
    member_count = serializers.IntegerField(read_only=True)  # MYA
    ticket_count = serializers.IntegerField(read_only=True)  # MYA
    tasks_to_do_count = serializers.IntegerField(read_only=True)  # MYA
    tasks_high_prio_count = serializers.IntegerField(read_only=True)  # MYA
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)  # MYA

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]  # MYA


class BoardSerializer(serializers.ModelSerializer):  # MYA (für POST/PATCH)
    member_count = serializers.SerializerMethodField()  # MYA
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)  # MYA

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "owner_id", "members"]  # MYA

    def get_member_count(self, obj):
        return obj.members.count()


class BoardMemberSerializer(serializers.ModelSerializer):  # MYA
    fullname = serializers.SerializerMethodField()  # MYA

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]  # MYA

    def get_fullname(self, obj):  # MYA
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name or getattr(obj, "fullname", "") or obj.username  # MYA


class BoardDetailSerializer(serializers.ModelSerializer):  # MYA
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)  # MYA
    members = BoardMemberSerializer(many=True, read_only=True)  # MYA
    tasks = serializers.SerializerMethodField()  # MYA

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]  # MYA

    def get_tasks(self, board):  # MYA
        rel = getattr(board, "tasks", None)
        qs = rel.all() if rel else []
        return [self._task_dict(t) for t in qs]  # MYA

    def _task_dict(self, t):  # MYA
        # MYA: defensiv -> wenn Feld fehlt, kommt None statt Crash
        return {
            "id": getattr(t, "id", None),
            "title": getattr(t, "title", None),
            "description": getattr(t, "description", ""),
            "status": getattr(t, "status", None),
            "priority": getattr(t, "priority", None),
            "assignee": self._user(getattr(t, "assignee", None) or getattr(t, "assigned_to", None)),
            "reviewer": self._user(getattr(t, "reviewer", None)),
            "due_date": getattr(t, "due_date", None),
            "comments_count": self._comments_count(t),
        }

    def _user(self, u):  # MYA
        return BoardMemberSerializer(u).data if u else None  # MYA

    def _comments_count(self, t):  # MYA
        rel = getattr(t, "comments", None) or getattr(t, "comment_set", None)
        return rel.count() if rel else 0  # MYA