"""Challenges app configuration for Django project."""
from django.apps import AppConfig


class ChallengesConfig(AppConfig):
    """Configuration for the Challenges app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'challenges'
