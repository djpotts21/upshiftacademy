"""URL configuration for the courses app."""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.programme_list, name='programme_list'),
    path('programme/<int:pk>/', views.programme_detail, name='programme_detail'),
    path('unit/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
]
