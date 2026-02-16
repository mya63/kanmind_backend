# MYA: registration gehört in authentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request):
    # MYA
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if not username or not password:
        return Response({"detail": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"detail": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_201_CREATED)
