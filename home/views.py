'''
home/views.py
Views for the home app.
This module contains the view functions for the home app,
rendering the home page and handling requests.
'''

from django.shortcuts import render


def home(request):
    """
    Render the home page.
    """
    return render(request, 'home/home.html')
