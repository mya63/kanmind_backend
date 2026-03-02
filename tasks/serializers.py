# tasks/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

from boards.models import Board  # MYA
from .models import Task, Comment  # MYA


def _fullname(user: User) -> str:
    name = f"{user.first_name} {user.last_name}".strip()
    return name if name else user.username


class UserMiniSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        return _fullname(obj)


class TaskSerializer(serializers.ModelSerializer):
    # OUTPUT (Doku): assignee/reviewer als Objekt
    assignee = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    # INPUT (Doku): assignee_id / reviewer_id
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assignee",
        required=False,
        allow_null=True,
        write_only=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        required=False,
        allow_null=True,
        write_only=True,
    )

    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)  # MYA: darf nie required sein

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "assignee_id",
            "reviewer_id",
            "due_date",
            "comments_count",
            "created_by",
        ]

    def get_assignee(self, obj):
        return UserMiniSerializer(obj.assignee).data if obj.assignee else None

    def get_reviewer(self, obj):
        return UserMiniSerializer(obj.reviewer).data if obj.reviewer else None

    def get_comments_count(self, obj):
        return obj.comments.count()

    def _is_board_member(self, board: Board, user: User) -> bool:
        if board.owner_id == user.id:
            return True
        return board.members.filter(id=user.id).exists()

    def validate(self, attrs):
        # Board kommt bei Create aus attrs, bei Update aus instance
        board = attrs.get("board", getattr(self.instance, "board", None))

        assignee = attrs.get("assignee", getattr(self.instance, "assignee", None))
        reviewer = attrs.get("reviewer", getattr(self.instance, "reviewer", None))

        if board and assignee and not self._is_board_member(board, assignee):
            raise serializers.ValidationError({"assignee_id": "Assignee muss Mitglied des Boards sein."})

        if board and reviewer and not self._is_board_member(board, reviewer):
            raise serializers.ValidationError({"reviewer_id": "Reviewer muss Mitglied des Boards sein."})

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user  # MYA: serverseitig setzen
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # MYA: Doku -> Board darf NICHT geändert werden
        validated_data.pop("board", None)
        return super().update(instance, validated_data)
    
    def validate_status(self, value):
        # MYA: Tests schicken "todo", Doku erwartet "to-do"
        mapping = {
            "todo": "to-do",
            "to_do": "to-do",
            "inprogress": "in-progress",
            "in_progress": "in-progress",
        }
        return mapping.get(value, value)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def get_author(self, obj):
        return _fullname(obj.author)