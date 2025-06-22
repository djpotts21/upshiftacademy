'''
home/urls.py
# URL configuration for the home app.
This module defines the URL patterns for the home app,
allowing the app to handle requests and route them to the appropriate views.
'''
from django.urls import path
from . import views


urlpatterns = [
    # Example:
    # path('', views.home, name='home'),
    path('', views.home, name='home'),  # Home page view
]
