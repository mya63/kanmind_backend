import pytest
from rest_framework.test import APIClient


def _auth_client(email="board@mail.de"):
    client = APIClient()
    reg = client.post("/api/registration/", {
        "fullname": "boarduser",
        "email": email,
        "password": "testpass123",
        "repeated_password": "testpass123"
    }, format="json")

    token = reg.data["token"]
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client


@pytest.mark.django_db
def test_create_board_and_list_boards():
    client = _auth_client()

    create = client.post("/api/boards/", {"title": "My Board"}, format="json")
    assert create.status_code == 201

    listing = client.get("/api/boards/")
    assert listing.status_code == 200
    assert len(listing.data) >= 1


@pytest.mark.django_db
def test_patch_board_updates_title():
    client = _auth_client()

    create = client.post("/api/boards/", {"title": "Old"}, format="json")
    assert create.status_code == 201
    board_id = create.data["id"]

    patch = client.patch(f"/api/boards/{board_id}/", {"title": "New"}, format="json")
    assert patch.status_code == 200
    assert patch.data["title"] == "New"


@pytest.mark.django_db
def test_patch_board_rejects_invalid_members_type():
    client = _auth_client()

    create = client.post("/api/boards/", {"title": "B1"}, format="json")
    board_id = create.data["id"]

    # members muss list sein -> invalid: string
    patch = client.patch(f"/api/boards/{board_id}/", {"members": "1"}, format="json")
    assert patch.status_code == 400