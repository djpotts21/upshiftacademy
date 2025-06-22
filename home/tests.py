'''
Tests for the home app views.
This module contains unit tests for the views in the home app,
ensuring they return the correct responses and render the expected templates.
from django.urls import reverse
'''

from django.urls import reverse


def test_home_view(self):
    """Test the home view to ensure it returns a 200 status code
    and uses the correct template"""
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'home/home.html')
