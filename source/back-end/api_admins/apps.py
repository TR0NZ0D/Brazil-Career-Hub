"""
api_admins/apps.py

Created by: Gabriel Menezes de Antonio
"""
from django.apps import AppConfig


class ApiAdminsConfig(AppConfig):
    """App config for api_admins module"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_admins'
    verbose_name = "API Admins"
