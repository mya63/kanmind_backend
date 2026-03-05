import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_registration_returns_token():
    client = APIClient()

    res = client.post(
        "/api/registration/",
        {
            "fullname": "testuser1",
            "email": "test1@mail.de",
            "password": "testpass123",
            "repeated_password": "testpass123",
        },
        format="json",
    )

    assert res.status_code == 201
    assert "token" in res.data
    assert "fullname" in res.data
    assert "email" in res.data
    assert "user_id" in res.data


@pytest.mark.django_db
def test_login_returns_token():
    client = APIClient()

    # Register first
    reg = client.post(
        "/api/registration/",
        {
            "fullname": "testuser2",
            "email": "test2@mail.de",
            "password": "testpass123",
            "repeated_password": "testpass123",
        },
        format="json",
    )
    assert reg.status_code == 201

    # Login (spec: email + password)
    res = client.post(
        "/api/login/",
        {"email": "test2@mail.de", "password": "testpass123"},
        format="json",
    )

    assert res.status_code == 200
    assert "token" in res.data
    assert "fullname" in res.data
    assert "email" in res.data
    assert "user_id" in res.data


@pytest.mark.django_db
def test_registration_unhappy_path_returns_400_instead_of_500():
    client = APIClient()

    # Missing required fields -> must return 400
    res = client.post("/api/registration/", {"email": "x@test.de"}, format="json")
    assert res.status_code == 400

    # Even with form-style payload, it must return 400 (not 500)
    res2 = client.post("/api/registration/", {"email": "x@test.de"})
    assert res2.status_code == 400