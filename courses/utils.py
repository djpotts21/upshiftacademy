"""Utility functions for course-related views."""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Programme


def student_required_for_programme(obj_lookup):
    """Decorator to ensure that the user is a student of the programme associated with the object."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, pk, *args, **kwargs):
            obj = get_object_or_404(obj_lookup['model'], pk=pk)
            programme = obj_lookup['get_programme'](obj)

            if request.user not in programme.students.all():
                return render(request, "courses/not_registered_on_course.html", {
                    "error": "You must be a student of this programme to view this content.",
                    "programmes": Programme.objects.all()
                })

            return view_func(request, pk, *args, **kwargs)
        return _wrapped_view
    return decorator
