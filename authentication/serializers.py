# authentication/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        fullname = validated_data["fullname"]
        email = validated_data["email"]
        password = validated_data["password"]

        user = User.objects.create_user(
            username=fullname,
            email=email,
            password=password
        )

        return user