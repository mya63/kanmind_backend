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