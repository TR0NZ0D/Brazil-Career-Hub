"""
api/urls.py

Created by: Gabriel Menezes de Antonio
"""
from django.urls import include, path

from . import views

app_name = 'api'

# localhost:8000/api/
urlpatterns = [
    # ========== API Info ========== #
    path('info/status/', views.ApiStatus.as_view()),  # type: ignore
    path('info/version/', views.ApiVersion.as_view()),  # type: ignore

    # ========== Authentication ========== #
    path('auth/', include('api_admins.urls')),  # type: ignore

    # ========== Users ========== #
    path('users/', include('users.urls')),

    # ========== Company ========== #
    path('company/', include('company.urls')),
]
