from django.contrib.auth.models import User
from rest_framework import serializers
from boards.models import Board


class BoardListSerializer(serializers.ModelSerializer):
    """
    Serializer for board list responses including aggregated counts.
    """

    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

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
        ]


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer used for board creation.
    """

    member_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "owner_id", "members"]

    def get_member_count(self, obj):
        return obj.members.count()


class BoardMemberSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for board members.
    """

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name or getattr(obj, "fullname", "") or obj.username


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for board detail responses including tasks.
    """

    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    members = BoardMemberSerializer(many=True, read_only=True)
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]

    def get_tasks(self, board):
        rel = getattr(board, "tasks", None)
        qs = rel.all() if rel else []
        return [self._task_dict(t) for t in qs]

    def _task_dict(self, task):
        """
        Defensive mapping of task fields.
        Missing attributes return None instead of raising errors.
        """
        return {
            "id": getattr(task, "id", None),
            "title": getattr(task, "title", None),
            "description": getattr(task, "description", ""),
            "status": getattr(task, "status", None),
            "priority": getattr(task, "priority", None),
            "assignee": self._user(getattr(task, "assignee", None) or getattr(task, "assigned_to", None)),
            "reviewer": self._user(getattr(task, "reviewer", None)),
            "due_date": getattr(task, "due_date", None),
            "comments_count": self._comments_count(task),
        }

    def _user(self, user):
        return BoardMemberSerializer(user).data if user else None

    def _comments_count(self, task):
        rel = getattr(task, "comments", None) or getattr(task, "comment_set", None)
        return rel.count() if rel else 0


class BoardPatchSerializer(serializers.ModelSerializer):
    """
    Serializer used for PATCH updates on boards.
    """

    owner_data = BoardMemberSerializer(source="owner", read_only=True)
    members_data = BoardMemberSerializer(source="members", many=True, read_only=True)

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Board
        fields = ["id", "title", "members", "owner_data", "members_data"]

    def update(self, instance, validated_data):
        if "title" in validated_data:
            instance.title = validated_data["title"]
            instance.save()

        if "members" in validated_data:
            users = validated_data.get("members") or []
            instance.members.set(users)
            instance.members.add(instance.owner)

        return instance