"""
company/urls.py

Created by: Gabriel Menezes de Antonio
"""
from django.urls import path

from . import views

app_name = 'company'

# localhost:8000/api/company/
urlpatterns = [
    # ========== Company Account ========== #
    path('', views.CompanyAccount.as_view()),  # type: ignore

    # ========== Company Profile ========== #
    path('profile/', views.CompanyProfile.as_view()),  # type: ignore

    # ========== Company Authentication ========== #
    path('auth/', views.CompanyAuth.as_view()),  # type: ignore
]
