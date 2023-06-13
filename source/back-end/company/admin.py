"""
company/admin.py

Created by: Gabriel Menezes de Antonio
"""

from django.contrib import admin

from . import models


class CompanyAccountAdmin(admin.ModelAdmin):
    """Admin model for company account"""
    list_display = ("cnpj", 'slug', 'registration_status', 'cnae', 'legal_nature')
    list_display_links = ("cnpj", 'slug')
    list_per_page = 50
    list_filter = ('registration_status', 'legal_nature')
    search_fields = ('corporate_name', 'fantasy_name', 'cnae')
    readonly_fields = ("slug",)


admin.site.register(models.CompanyAccountModel, CompanyAccountAdmin)
