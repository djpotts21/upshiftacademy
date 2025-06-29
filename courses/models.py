"""
Django models for courses, including modules, lessons, units, and programmes.
These models are designed to be used in a learning management system (LMS).
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# pylint: disable=invalid-str-returned


class Module(models.Model):
    """Model representing a course module."""
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(upload_to='modules/', blank=True, null=True)
    video = models.FileField(upload_to='modules/videos/', blank=True, null=True)
    resources = models.FileField(upload_to='modules/resources/', blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    challenges = models.ManyToManyField('challenges.CodeChallenge', related_name='modules', blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Model representing a lesson composed of multiple modules."""
    title = models.CharField(max_length=255)
    modules = models.ManyToManyField(Module, related_name='lessons')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, help_text="Description of the unit in the context of the programme.")


    def __str__(self):
        return self.title


class Unit(models.Model):
    """Model representing a unit containing multiple lessons."""
    title = models.CharField(max_length=255)
    lessons = models.ManyToManyField(Lesson, related_name='units')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, help_text="Description of the unit in the context of the programme.")


    def __str__(self):
        return self.title


class ProgrammeUnit(models.Model):
    """Intermediate model to associate programmes with units."""
    programme = models.ForeignKey('Programme', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, help_text="Description of the unit in the context of the programme.")

    class Meta:
        unique_together = ('programme', 'unit')
        ordering = ['order']

    def __str__(self):
        return f"{self.programme.title} > {self.unit.title} (Order: {self.order})"


class PrerequisiteProgrammes(models.Model):
    """Model to represent prerequisite programmes for a unit."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
 
    def __str__(self):
        return self.title


class Programme(models.Model):
    """Model representing a programme containing multiple units."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='programmes/heroes/', blank=True, null=True)
    video = models.FileField(upload_to='programmes/videos/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    length = models.PositiveIntegerField(
        help_text="Length in weeks", default=0
    )
    prerequisites = models.ManyToManyField(
        PrerequisiteProgrammes,
        related_name='programmes',
        blank=True
    )
    units = models.ManyToManyField(
        'Unit', through='ProgrammeUnit', related_name='programmes')
    tutors = models.ManyToManyField(User, related_name='programmes')
    students = models.ManyToManyField(
        User, related_name='programmes_as_student', blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    """Student submission tied to a unit, lesson, or module."""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)

    content = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    grade = models.IntegerField(null=True, blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    graded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} - {self.unit.title} ({self.submitted_at.date()})"
