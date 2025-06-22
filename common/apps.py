'''
Django application configuration for the common app.
'''
from django.apps import AppConfig


class CommonConfig(AppConfig):
    """ Configuration class for the common app. """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    def ready(self):
        import common.signals  # noqa: F401, E501  # pylint: disable=unused-import, import-outside-toplevel
