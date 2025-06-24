"""URL configuration for the code challenges app."""
from django.urls import path
from .views import run_code_challenge, run_code_ajax

urlpatterns = [
    path('<int:challenge_id>/', run_code_challenge, name='run_code_challenge'),
    path('run_code/<int:challenge_id>/', run_code_ajax, name='run_code_ajax'),
]
