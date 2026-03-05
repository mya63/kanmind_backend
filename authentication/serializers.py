from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    """
    Validate registration data and create a Django User.
    """

    fullname = serializers.CharField(max_length=150, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(write_only=True, min_length=6)
    repeated_password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return email

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("repeated_password"):
            raise serializers.ValidationError({"repeated_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        # Use fullname as username (simple and stable for tests)
        fullname = validated_data["fullname"].strip()
        email = validated_data["email"].strip().lower()
        password = validated_data["password"]

        return User.objects.create_user(
            username=fullname,
            email=email,
            password=password,
        )