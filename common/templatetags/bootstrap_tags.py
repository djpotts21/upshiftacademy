'''
This module provides a custom template filter to convert Django message tags
into Bootstrap alert classes.
'''
from django import template

register = template.Library()


@register.filter
def bootstrap_alert_class(tag):
    """Convert Django message tags to Bootstrap alert classes."""
    if tag == 'error':
        return 'danger'
    return tag
