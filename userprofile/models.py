'''
UserProfile model for storing user profile information.
This module defines the UserProfile model, which includes fields for user bio,
profile picture, location, date of birth,
and timestamps for creation and updates.
'''
from django.db import models


class UserProfile(models.Model):
    """UserProfile model"""
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Profile"
