'''
This module defines the URL patterns for the user profile app.
It includes paths for viewing and editing user profiles,
uploading profile pictures,deleting profile pictures,
updating profile information, and changing passwords.
'''
from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.profileedit,
         name='profile'
         ),
    path('<int:userid>/',
         views.public_profile,
         name='public_profile'
         ),
    path('uploadprofilephoto',
         views.upload_profile_picture,
         name='upload_profile_picture'
         ),
    path('deleteprofilepicture/',
         views.delete_profile_picture,
         name='delete_profile_picture'
         ),
    path('updateprofile/',
         views.update_profile,
         name='update_profile'
         ),
    path('updatepassword/',
         views.update_password,
         name='update_password'
         ),
]
