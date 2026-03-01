# authentication/views.py

# MYA: Auth Views nach Doku (registration + login)

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegistrationSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    token = Token.objects.create(user=user)

    return Response(
        {
            "token": token.key,
            "fullname": user.username,
            "email": user.email,
            "user_id": user.id
        },
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "")

    if not email or not password:
        return Response({"detail": "email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_obj = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({"detail": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=user_obj.username, password=password)
    if not user:
        return Response({"detail": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "token": token.key,
            "fullname": user.username,
            "email": user.email,
            "user_id": user.id
        },
        status=status.HTTP_200_OK
    )

class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email", "").strip()

        # Email fehlt
        if not email:
            return Response(
                {"detail": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Email Format prüfen
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"detail": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # User suchen
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response(
                {"detail": "Email not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        fullname = f"{user.first_name} {user.last_name}".strip() or user.username

        return Response(
            {
                "id": user.id,
                "email": user.email,
                "fullname": fullname
            },
            status=status.HTTP_200_OK
        )