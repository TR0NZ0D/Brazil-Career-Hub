"""
company/apps.py

Created by: Gabriel Menezes de Antonio
"""

from django.apps import AppConfig


class CompanyConfig(AppConfig):
    """Company app config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'company'
    verbose_name = "Company"
