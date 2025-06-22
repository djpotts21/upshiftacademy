'''
This file is part of the User Profile Management application.
It defines the configuration for the userprofile app,
which handles user profiles, including registration,
profile updates, and related functionalities.
'''
from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    """Configuration class for the 'userprofile' app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userprofile'
    verbose_name = 'User Profile Management'

    def ready(self):
        import common.signals  # noqa: F401, E501  # pylint: disable=unused-import, import-outside-toplevel
