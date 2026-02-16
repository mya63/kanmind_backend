from rest_framework import serializers
from boards.models import Board  # MYA

class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "owner_id", "members"]

    def get_member_count(self, obj):
        return obj.members.count()
