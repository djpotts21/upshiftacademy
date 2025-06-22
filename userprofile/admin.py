'''
Admin configuration for UserProfile model
This module registers the UserProfile model with the Django admin site,
customizing the admin interface to enhance user experience.
'''

from django.contrib import admin
from django.forms.widgets import DateInput
from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """Form for UserProfile model
    This form is used to create and update UserProfile
    instances in the admin interface.
    It includes a custom date input widget for the date_of_birth field.
    """
    class Meta:
        """Meta class for UserProfileForm"""
        model = UserProfile
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(
                format='%d/%m/%Y', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dob = self.initial.get('date_of_birth')
        if dob and not isinstance(dob, str):
            self.initial['date_of_birth'] = dob.strftime('%Y-%m-%d')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model
    This class customizes the admin interface for the UserProfile model,
    including the form used for creating and updating profiles,
    the fields displayed in the list view, and the search functionality.
    """
    form = UserProfileForm
    list_display = ('user',)
    search_fields = ('user__username',)
    list_filter = ('user__is_active', 'user__is_staff')
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'bio',
                'profile_picture',
                'location',
                'date_of_birth',
            )
        }),
    )
