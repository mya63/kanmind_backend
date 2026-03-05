# boards/admin.py

from django.contrib import admin
from boards.models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Admin configuration for Board model.
    """

    list_display = ("id", "title", "owner", "created_at")
    search_fields = ("title", "owner__username", "owner__email")
    list_filter = ("created_at",)