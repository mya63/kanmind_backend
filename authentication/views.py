from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


# NEU: feste Guest-Login-Daten passend zum Frontend
GUEST_EMAIL = "kevin@kovacsi.de"
GUEST_PASSWORD = "asdasdasd"
GUEST_USERNAME = "Demo User"


# NEU: erstellt den Guest-User automatisch, falls er auf Render fehlt
def get_or_create_guest_user():
    user, created = User.objects.get_or_create(
        email=GUEST_EMAIL,
        defaults={"username": GUEST_USERNAME},
    )

    if created or not user.check_password(GUEST_PASSWORD):
        user.username = GUEST_USERNAME
        user.set_password(GUEST_PASSWORD)
        user.save()

    return user


@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request):
    """
    Register a new user and return an auth token.
    """
    payload = request.data if isinstance(request.data, dict) else {}

    serializer = RegistrationSerializer(data=payload)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "token": token.key,
            "fullname": user.username,
            "email": user.email,
            "user_id": user.id,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Login using email + password and return an auth token.
    """
    email = request.data.get("email", "").strip().lower()
    password = request.data.get("password", "")

    if not email or not password:
        return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # NEU: Guest Login funktioniert direkt beim Klick
    if email == GUEST_EMAIL and password == GUEST_PASSWORD:
        user = get_or_create_guest_user()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "fullname": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )

    user_obj = User.objects.filter(email__iexact=email).first()
    if not user_obj:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=user_obj.username, password=password)
    if not user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "token": token.key,
            "fullname": user.username,
            "email": user.email,
            "user_id": user.id,
        },
        status=status.HTTP_200_OK,
    )


class EmailCheckView(APIView):
    """
    Protected endpoint to validate an email and return user basics if found.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email", "").strip()

        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({"detail": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({"detail": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

        fullname = f"{user.first_name} {user.last_name}".strip() or user.username

        return Response(
            {"id": user.id, "email": user.email, "fullname": fullname},
            status=status.HTTP_200_OK,
        )