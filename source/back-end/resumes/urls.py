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
    path('resumes/', views.Resume.as_view()),  # type: ignore

    # ========== Experience ========== #
    path('resumes/experience/', views.Experience.as_view()),  # type: ignore

    # ========== Competence ========== #
    path('resumes/competence/', views.Competence.as_view()),  # type: ignore

    # ========== Course ========== #
    path('resumes/course/', views.Course.as_view()),  # type: ignore

    # ========== Reference ========== #
    path('resumes/reference/', views.Reference.as_view()),  # type: ignore

    # ========== Graduation ========== #
    path('resumes/graduation/', views.Graduation.as_view()),  # type: ignore

    # ========== Project ========== #
    path('resumes/project/', views.Project.as_view()),  # type: ignore

    # ========== Link ========== #
    path('resumes/link/', views.Link.as_view())  # type: ignore
]
