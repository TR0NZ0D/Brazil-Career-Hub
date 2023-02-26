"""
api/apps.py

Created by: Gabriel Menezes de Antonio
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """App config for django modules"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'API'
