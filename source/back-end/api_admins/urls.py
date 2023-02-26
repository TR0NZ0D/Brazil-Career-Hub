"""
api_admins/urls.py

Created by: Gabriel Menezes de Antonio
"""
from django.urls import path

from . import views

app_name = 'api_admins'


urlpatterns = [
    # ========== Token ========== #
    path('token/', views.BaseAuthToken.as_view()),  # type: ignore
]
