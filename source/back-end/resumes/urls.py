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
    path('', views.Resume.as_view()),  # type: ignore

    # ========== Experience ========== #
    path('experience/', views.Experience.as_view()),  # type: ignore

    # ========== Competence ========== #
    path('competence/', views.Competence.as_view()),  # type: ignore

    # ========== Course ========== #
    path('course/', views.Course.as_view()),  # type: ignore

    # ========== Reference ========== #
    path('reference/', views.Reference.as_view()),  # type: ignore

    # ========== Graduation ========== #
    path('graduation/', views.Graduation.as_view()),  # type: ignore

    # ========== Project ========== #
    path('project/', views.Project.as_view()),  # type: ignore

    # ========== Link ========== #
    path('link/', views.Link.as_view())  # type: ignore
]
