"""
users/urls.py

Created by: Gabriel Menezes de Antonio
"""
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # ========== Badges ========== #
    path('badges/', views.UserBadges.as_view()),  # type: ignore

    # ========== Bans ========== #
    path('bans/', views.BannedUsers.as_view()),  # type: ignore

    # ========== Profile ========== #
    path('profile/', views.UserProfile.as_view()),  # type: ignore
]
