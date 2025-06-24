"""Admin configuration for CodeChallenge model.
Registers the CodeChallenge model with the Django admin interface."""
from django.contrib import admin
from .models import CodeChallenge, CodeSubmission


@admin.register(CodeChallenge)
class CodeChallengeAdmin(admin.ModelAdmin):
    """Admin configuration for CodeChallenge model."""
    list_display = ('title', 'lesson', 'created_by', 'created_at')
    search_fields = ('title', 'instructions')


@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for CodeSubmission model."""
    list_display = ('student', 'challenge', 'passed', 'created_at')
    search_fields = ('student__username', 'challenge__title')
    list_filter = ('passed', 'created_at')
