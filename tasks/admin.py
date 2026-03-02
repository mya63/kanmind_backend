# tasks/admin.py

from django.contrib import admin
from tasks.models import Task, Comment  # MYA

admin.site.register(Task)
admin.site.register(Comment)