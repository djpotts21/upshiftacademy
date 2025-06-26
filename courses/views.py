"""Django view to display a programme detail page"""

from django.shortcuts import render, get_object_or_404
from .models import Programme, Unit, Lesson, Module
from .utils import student_required_for_programme


def programme_list(request):
    """View to display a list of programmes."""
    programmes = Programme.objects.all()
    return render(request, "courses/programme_list.html", {"programmes": programmes})


def programme_detail(request, pk):
    """View to display the details of a programme."""
    programme = get_object_or_404(Programme, pk=pk)
    return render(request, "courses/programme_detail.html", {"programme": programme})


def unit_detail(request, pk):
    """View to display the details of a unit."""
    unit = get_object_or_404(Unit, pk=pk)
    programme_unit = unit.programmeunit_set.first()
    programme = programme_unit.programme if programme_unit else None
    return render(request, "courses/unit_detail.html", {"unit": unit, "programme": programme})


def lesson_detail(request, pk):
    """View to display the details of a lesson."""
    lesson = get_object_or_404(Lesson, pk=pk)
    # Assuming each lesson is associated with a unit
    unit = lesson.units.first()
    return render(request, "courses/lesson_detail.html", {"lesson": lesson,  "unit": unit})


@student_required_for_programme({
    'model': Module,
    'get_programme': lambda module: Programme.objects.filter(units__lessons__modules=module).first()
})
def module_detail(request, pk):
    """View to display the details of a module."""
    module = get_object_or_404(Module, pk=pk)
    lesson = module.lessons.first()  # Get the first lesson in the module
    return render(request, "courses/module_detail.html", {"module": module, "lesson": lesson})