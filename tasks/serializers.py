from django.contrib.auth.models import User
from rest_framework import serializers

from boards.models import Board
from tasks.models import Task, Comment


def _fullname(user: User) -> str:
    """
    Return the full name of a user if available,
    otherwise fall back to the username.
    """
    name = f"{user.first_name} {user.last_name}".strip()
    return name if name else user.username


class UserMiniSerializer(serializers.ModelSerializer):
    """
    Minimal user serializer used in task responses.
    """

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        return _fullname(obj)


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks.

    Output:
    - assignee and reviewer as nested user objects
    - comments_count

    Input:
    - assignee_id
    - reviewer_id
    """

    assignee = serializers.SerializerMethodField()
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

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
        """
        Check if a user is the board owner or a member.
        """
        if board.owner_id == user.id:
            return True
        return board.members.filter(id=user.id).exists()

    def validate(self, attrs):
        board = attrs.get("board", getattr(self.instance, "board", None))
        assignee = attrs.get("assignee", getattr(self.instance, "assignee", None))
        reviewer = attrs.get("reviewer", getattr(self.instance, "reviewer", None))

        if self.instance and "board" in attrs:
            raise serializers.ValidationError({"board": "Board cannot be changed."})

        if board and assignee and not self._is_board_member(board, assignee):
            raise serializers.ValidationError(
                {"assignee_id": "Assignee must be a board member."}
            )

        if board and reviewer and not self._is_board_member(board, reviewer):
            raise serializers.ValidationError(
                {"reviewer_id": "Reviewer must be a board member."}
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("board", None)
        return super().update(instance, validated_data)

    def validate_status(self, value):
        """
        Normalize common status variations.
        """
        mapping = {
            "todo": "to-do",
            "to_do": "to-do",
            "inprogress": "in-progress",
            "in_progress": "in-progress",
        }
        return mapping.get(value, value)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for task comments.
    """

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def get_author(self, obj):
        return _fullname(obj.author)