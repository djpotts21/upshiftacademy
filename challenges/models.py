"""models.py
Defines the CodeChallenge model for grading code challenges in lessons."""
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Lesson


User = get_user_model()
# pylint: disable=invalid-str-returned,
# pylint: disable=unused-variable, no-member, unused-argument
# flake8: noqa


class CodeChallenge(models.Model):
    """Code challenge tied to a lesson, with test file and expected outputs."""
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    starter_code = models.TextField(blank=True, null=True)
    test_code = models.TextField(blank=True, null=True)
    expected_output = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # noqa: D105,D401
        return self.title


class CodeSubmission(models.Model):
    """Stores each student submission for a challenge."""
    challenge = models.ForeignKey(
        CodeChallenge, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.TextField()
    output = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.challenge.title} ({'✅' if self.passed else '❌'})"
