import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_registration_returns_token():
    client = APIClient()

    res = client.post("/api/registration/", {
        "fullname": "testuser1",
        "email": "test1@mail.de",
        "password": "testpass123",
        "repeated_password": "testpass123"
    }, format="json")

    assert res.status_code == 201
    assert "token" in res.data
    assert "fullname" in res.data
    assert "email" in res.data
    assert "user_id" in res.data


@pytest.mark.django_db
def test_login_returns_token():
    client = APIClient()

    # Registrierung
    reg = client.post("/api/registration/", {
        "fullname": "testuser2",
        "email": "test2@mail.de",
        "password": "testpass123",
        "repeated_password": "testpass123"
    }, format="json")

    assert reg.status_code == 201

    # Login (laut Doku: email + password)
    res = client.post("/api/login/", {
        "email": "test2@mail.de",
        "password": "testpass123"
    }, format="json")

    assert res.status_code == 200
    assert "token" in res.data
    assert "fullname" in res.data
    assert "email" in res.data
    assert "user_id" in res.data