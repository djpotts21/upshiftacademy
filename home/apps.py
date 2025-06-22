'''
Django application configuration for the 'home' app.
This module defines the configuration class for the 'home' app,
which is responsible for managing the app's settings and behavior
within the Django project.
'''

from django.apps import AppConfig


class MembersConfig(AppConfig):
    """Configuration class for the 'home' app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
