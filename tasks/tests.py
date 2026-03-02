# tasks/tests.py

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from boards.models import Board
from tasks.models import Task, Comment


@pytest.fixture
def user_a(db):
    return User.objects.create_user(username="user_a", email="a@test.de", password="pass12345")


@pytest.fixture
def user_b(db):
    return User.objects.create_user(username="user_b", email="b@test.de", password="pass12345")


@pytest.fixture
def board(db, user_a):
    b = Board.objects.create(title="Board 1", owner=user_a)
    b.members.add(user_a)
    return b


@pytest.fixture
def auth_a(user_a):
    client = APIClient()  # FIX: eigener Client pro User
    client.force_authenticate(user=user_a)
    return client


@pytest.fixture
def auth_b(user_b):
    client = APIClient()  # FIX: eigener Client pro User
    client.force_authenticate(user=user_b)
    return client


@pytest.mark.django_db
def test_assigned_to_me_only_returns_assigned(auth_a, board, user_a, user_b):
    board.members.add(user_b)
    Task.objects.create(board=board, title="T1", created_by=user_a, assignee=user_a)
    Task.objects.create(board=board, title="T2", created_by=user_a, assignee=user_b)

    res = auth_a.get("/api/tasks/assigned-to-me/")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["title"] == "T1"


@pytest.mark.django_db
def test_create_task_requires_board_member(auth_b, board):
    payload = {"board": board.id, "title": "X", "status": "to-do", "priority": "low"}
    res = auth_b.post("/api/tasks/", payload, format="json")
    assert res.status_code == 400 or res.status_code == 403


@pytest.mark.django_db
def test_delete_comment_only_author(auth_a, auth_b, board, user_a, user_b):
    board.members.add(user_b)
    task = Task.objects.create(board=board, title="T", created_by=user_a)
    comment = Comment.objects.create(task=task, author=user_a, content="hi")

    res = auth_b.delete(f"/api/tasks/{task.id}/comments/{comment.id}/")
    assert res.status_code == 403

    res2 = auth_a.delete(f"/api/tasks/{task.id}/comments/{comment.id}/")
    assert res2.status_code == 204


# ------------------------------
# MYA: Coverage-Tests für Views
# ------------------------------

@pytest.mark.django_db
def test_tasks_list_only_board_members(auth_a, auth_b, board, user_a):
    Task.objects.create(board=board, title="T1", created_by=user_a)

    # user_b ist kein Member
    res = auth_b.get("/api/tasks/")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.django_db
def test_task_detail_forbidden_if_not_member(auth_a, auth_b, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_b.get(f"/api/tasks/{task.id}/")
    assert res.status_code == 403


@pytest.mark.django_db
def test_task_detail_404_if_not_exists(auth_a):
    res = auth_a.get("/api/tasks/999999/")
    assert res.status_code == 404


@pytest.mark.django_db
def test_delete_task_only_creator_or_board_owner(auth_a, auth_b, board, user_a, user_b):
    board.members.add(user_b)
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    # user_b ist Member, aber nicht Creator und nicht Owner
    res = auth_b.delete(f"/api/tasks/{task.id}/")
    assert res.status_code == 403

    # creator darf löschen
    res2 = auth_a.delete(f"/api/tasks/{task.id}/")
    assert res2.status_code in (204, 200)


@pytest.mark.django_db
def test_patch_task_rejects_invalid_status(auth_a, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a, status="to-do")

    # ungültiger status -> sollte 400 geben
    res = auth_a.patch(f"/api/tasks/{task.id}/", {"status": "not-a-status"}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_comment_list_forbidden_if_not_member(auth_a, auth_b, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_b.get(f"/api/tasks/{task.id}/comments/")
    assert res.status_code == 403

@pytest.mark.django_db
def test_assigned_to_me_empty(auth_a):
    res = auth_a.get("/api/tasks/assigned-to-me/")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.django_db
def test_reviewing_filter(auth_a, board, user_a):
    task = Task.objects.create(
        board=board,
        title="Review Task",
        created_by=user_a,
        reviewer=user_a
    )

    res = auth_a.get("/api/tasks/reviewing/")
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.django_db
def test_cannot_change_board_on_patch(auth_a, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    new_board = Board.objects.create(title="Other", owner=user_a)
    new_board.members.add(user_a)

    res = auth_a.patch(
        f"/api/tasks/{task.id}/",
        {"board": new_board.id},
        format="json"
    )

    assert res.status_code == 400 or res.status_code == 403


@pytest.mark.django_db
def test_comment_create_forbidden_if_not_member(auth_a, auth_b, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_b.post(
        f"/api/tasks/{task.id}/comments/",
        {"content": "x"},
        format="json"
    )

    assert res.status_code == 403

# ------------------------------
# MYA: More coverage for tasks/views.py
# ------------------------------

@pytest.mark.django_db
def test_create_task_without_board_creates_default_board(auth_a, user_a):
    # kein Board übergeben -> Default Board wird erstellt
    res = auth_a.post(
        "/api/tasks/",
        {"title": "No board", "status": "todo", "priority": "low"},
        format="json",
    )
    assert res.status_code == 201
    assert Board.objects.filter(owner=user_a, title="Default Board").exists()


@pytest.mark.django_db
def test_create_task_forbidden_if_not_member_even_when_board_given(auth_a, auth_b, board):
    # board gehört user_a, user_b ist kein Member
    res = auth_b.post(
        "/api/tasks/",
        {"board": board.id, "title": "X", "status": "todo", "priority": "low"},
        format="json",
    )
    assert res.status_code == 403


@pytest.mark.django_db
def test_comment_create_empty_content_returns_400(auth_a, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_a.post(
        f"/api/tasks/{task.id}/comments/",
        {"content": "   "},
        format="json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_delete_comment_404_if_not_found(auth_a, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_a.delete(f"/api/tasks/{task.id}/comments/999999/")
    assert res.status_code == 404

@pytest.mark.django_db
def test_get_task_forbidden_if_not_member(auth_a, auth_b, board, user_a):
    task = Task.objects.create(board=board, title="Secret", created_by=user_a)
    res = auth_b.get(f"/api/tasks/{task.id}/")
    assert res.status_code == 403


@pytest.mark.django_db
def test_delete_task_forbidden_if_not_creator_or_owner(auth_a, auth_b, board, user_a, user_b):
    board.members.add(user_b)
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_b.delete(f"/api/tasks/{task.id}/")
    assert res.status_code == 403


@pytest.mark.django_db
def test_patch_task_invalid_data_returns_400(auth_a, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_a.patch(
        f"/api/tasks/{task.id}/",
        {"status": "invalid-status"},
        format="json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_get_comments_forbidden_if_not_member(auth_a, auth_b, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_b.get(f"/api/tasks/{task.id}/comments/")
    assert res.status_code == 403

@pytest.mark.django_db
def test_delete_task_as_board_owner(auth_a, auth_b, board, user_a, user_b):
    # user_a ist Owner des Boards
    board.members.add(user_b)
    task = Task.objects.create(board=board, title="T1", created_by=user_b)

    res = auth_a.delete(f"/api/tasks/{task.id}/")
    assert res.status_code == 204


@pytest.mark.django_db
def test_tasks_reviewing_filter(auth_a, board, user_a):
    Task.objects.create(board=board, title="T1", created_by=user_a, reviewer=user_a)
    Task.objects.create(board=board, title="T2", created_by=user_a)

    res = auth_a.get("/api/tasks/reviewing/")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["title"] == "T1"


@pytest.mark.django_db
def test_get_task_forbidden_if_not_member_or_owner(auth_a, auth_b, user_a):
    board = Board.objects.create(title="Secret", owner=user_a)
    task = Task.objects.create(board=board, title="Hidden", created_by=user_a)

    res = auth_b.get(f"/api/tasks/{task.id}/")
    assert res.status_code == 403

@pytest.mark.django_db
def test_tasks_list_owner_without_membership(auth_a, user_a):
    board = Board.objects.create(title="OwnerOnly", owner=user_a)
    Task.objects.create(board=board, title="T1", created_by=user_a)

    res = auth_a.get("/api/tasks/")
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.django_db
def test_create_task_invalid_serializer_returns_400(auth_a):
    res = auth_a.post(
        "/api/tasks/",
        {"status": "todo"},  # title fehlt
        format="json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_patch_task_invalid_title_returns_400(auth_a, board, user_a):
    task = Task.objects.create(board=board, title="Valid", created_by=user_a)

    res = auth_a.patch(
        f"/api/tasks/{task.id}/",
        {"title": ""},  # leerer Titel → ValidationError
        format="json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_get_comments_success(auth_a, board, user_a):
    task = Task.objects.create(board=board, title="T1", created_by=user_a)
    Comment.objects.create(task=task, author=user_a, content="Hi")

    res = auth_a.get(f"/api/tasks/{task.id}/comments/")
    assert res.status_code == 200
    assert len(res.json()) == 1