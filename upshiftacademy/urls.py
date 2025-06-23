'''
Django URL Configuration
This module defines the URL patterns for the Django project,
including the admin interface, user authentication, and app-specific URLs.
'''

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('userprofile.urls')),
    path('', include('home.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
