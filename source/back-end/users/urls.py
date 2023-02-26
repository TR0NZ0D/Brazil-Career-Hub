from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    # ========== Badges ========== #
    path('badges/', views.UserBadges.as_view()),  # type: ignore

    # ========== Bans ========== #
    path('bans/', views.BannedUsers.as_view()),  # type: ignore

    # ========== Profile ========== #
    path('profile/', views.UserProfile.as_view()),  # type: ignore
]
