# tasks/models.py

from django.db import models
from django.contrib.auth.models import User
from boards.models import Board  # MYA


class Task(models.Model):
    # MYA: Status + Priority exakt wie Doku
    STATUS_CHOICES = [
        ("to-do", "to-do"),
        ("in-progress", "in-progress"),
        ("review", "review"),
        ("done", "done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "low"),
        ("medium", "medium"),
        ("high", "high"),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")  # MYA
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")

    assignee = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tasks"
    )  # MYA
    reviewer = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="review_tasks"
    )  # MYA

    due_date = models.DateField(null=True, blank=True)  # MYA
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")  # MYA

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # MYA

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")  # MYA
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_comments")  # MYA
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on Task {self.task_id}"