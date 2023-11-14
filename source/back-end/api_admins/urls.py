"""
api_admins/urls.py

Created by: Gabriel Menezes de Antonio
"""
from django.urls import path

from . import views

app_name = 'api_admins'


# localhost:8000/api/auth/
urlpatterns = [
    # ========== Token ========== #
    path('token/', views.BaseAuthToken.as_view()),  # type: ignore
]
