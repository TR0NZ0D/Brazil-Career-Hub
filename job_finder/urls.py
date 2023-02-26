"""job_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view  # type: ignore

schema_url_patterns = [
    path('api/', include('api.urls'))
]

swagger_view = get_swagger_view(title="Job Finder - API",
                                patterns=schema_url_patterns)

urlpatterns = [
    # ========== API ========== #
    path('api/', include('api.urls')),
    path('api/docs/', swagger_view, name="swagger_docs"),  # type: ignore
    path('api/auth/', include('rest_framework.urls')),

    # ========== Django Built-In ========== #
    path('admin/', admin.site.urls),
]