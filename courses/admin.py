"""
Admin configuration for the courses app, restricting
access to tutors' own content.
"""
from django.contrib import admin
from .models import (
    Programme,
    Unit,
    Lesson,
    Module,
    Submission
)

# pylint: disable=unused-argument, no-self-use, too-few-public-methods


class TutorRestrictedAdmin(admin.ModelAdmin):
    """Base class for admin models that
    restrict access to tutors' own content."""
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_staff:
            return qs
        if request.user.groups.filter(name='tutors').exists():
            return qs.filter(created_by=request.user)
        return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if obj and hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


class ReadOnlyCreatedByMixin:
    """Mixin to display created_by field in read-only mode."""
    def save_model(self, request, obj, form, change):
        """Override save_model to set created_by field."""
        if not obj.pk:
            obj.created_by = request.user
        obj.save()


@admin.register(Module)
class ModuleAdmin(ReadOnlyCreatedByMixin, TutorRestrictedAdmin):
    """Admin for Module model with read-only created_by field."""
    list_display = ('title', 'created_by')
    exclude = ('created_by',)


@admin.register(Lesson)
class LessonAdmin(ReadOnlyCreatedByMixin, TutorRestrictedAdmin):
    """Admin for Lesson model with read-only created_by field."""
    list_display = ('title', 'created_by')
    filter_horizontal = ('modules',)
    exclude = ('created_by',)


@admin.register(Unit)
class UnitAdmin(ReadOnlyCreatedByMixin, TutorRestrictedAdmin):
    """Admin for Unit model with read-only created_by field."""
    list_display = ('title', 'created_by')
    filter_horizontal = ('lessons',)
    exclude = ('created_by',)


@admin.register(Programme)
class ProgrammeAdmin(ReadOnlyCreatedByMixin, TutorRestrictedAdmin):
    """Admin interface for the Programme model."""
    list_display = ('title', 'created_by', 'created_at')
    filter_horizontal = ('units', 'tutors',)
    exclude = ('created_by',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'unit', 'submitted_at', 'graded')
    list_filter = ('graded', 'unit', 'programme')
    search_fields = ('student__username', 'unit__title')