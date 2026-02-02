from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
  assigned_to = serializers.IntegerField(required=False, allow_null=True)
  reviewer = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = Task
    fields = "__all__"