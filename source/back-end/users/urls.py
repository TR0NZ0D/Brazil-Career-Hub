"""
users/urls.py

Created by: Gabriel Menezes de Antonio
"""
from django.urls import path

from . import views

app_name = 'users'

# localhost:8000/api/users/
urlpatterns = [
    # ========== User Management ========== #
    path("", views.UserManagement.as_view()),  # type: ignore

    # ========== Auth ========== #
    path("auth/", views.UserAuthentication.as_view()),  # type: ignore

    # ========== Bans ========== #
    path('bans/', views.BannedUsers.as_view()),  # type: ignore

    # ========== Profile ========== #
    path('profile/', views.UserProfile.as_view()),  # type: ignore
]
