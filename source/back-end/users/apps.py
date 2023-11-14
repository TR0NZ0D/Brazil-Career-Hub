"""
users/apps.py

Created by: Gabriel Menezes de Antonio
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """App config for user module"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "Users"
