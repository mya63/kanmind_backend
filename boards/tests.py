import pytest
from rest_framework.test import APIClient

def _auth_client():
    client = APIClient()

    reg = client.post("/api/registration/", {
        "fullname": "taskuser",
        "email": "task@mail.de",
        "password": "testpass123",
        "repeated_password": "testpass123"
    }, format="json")

    token = reg.data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    return client

@pytest.mark.django_db
def test_create_and_list_tasks():
    client = _auth_client()

    create = client.post("/api/tasks/", {
        "title": "My Task",
        "description": "Test",
        "status": "todo"
    }, format="json")
    assert create.status_code == 201

    listing = client.get("/api/tasks/")
    assert listing.status_code == 200
    assert len(listing.data) >= 1