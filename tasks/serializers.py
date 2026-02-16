from rest_framework import serializers
from django.contrib.auth.models import User
from tasks.models import Task  # MYA

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Task
        fields = "__all__"
