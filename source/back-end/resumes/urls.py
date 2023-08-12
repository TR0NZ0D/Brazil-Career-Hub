"""
resumes/urls.py

Created by: Gabriel Menezes de Antonio
"""
from django.urls import path

from . import views

app_name = 'resumes'

# localhost:8000/api/resumes/
urlpatterns = [
    # ========== Resumes ========== #
    path('resumes/', views.Resume.as_view())  # type: ignore
]
