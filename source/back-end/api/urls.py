from . import views
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from .tools.api_tools import generate_version, version, environment

app_name = 'api'

urlpatterns = [
    # ========== API Info ========== #
    path('info/status/', views.ApiStatus.as_view()),  # type: ignore
    path('info/version/', views.ApiVersion.as_view()),  # type: ignore

    # ========== Authentication ========== #
    path('auth/', include('api_admins.urls')),  # type: ignore

    # ========== Users ========== #
    path('users/', include('users.urls')),
]
