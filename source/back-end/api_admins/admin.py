"""
api_admins/admin.py

Created by: Gabriel Menezes de Antonio
"""
from django.contrib import admin

from . import models


class ApiAdminAdmin(admin.ModelAdmin):
    """Admin model for admin page"""
    list_display = ('user', 'token')
    list_display_links = ('user',)
    search_fields = ('user', 'token')
    readonly_fields = ('token',)
    list_per_page = 20


admin.site.register(models.ApiAdmin, ApiAdminAdmin)
