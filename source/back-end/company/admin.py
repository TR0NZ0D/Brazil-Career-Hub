"""
company/admin.py

Created by: Gabriel Menezes de Antonio
"""

from django.contrib import admin

from . import models


class CompanyAccountAdmin(admin.ModelAdmin):
    """Admin model for company account"""
    list_display = ("cnpj", 'slug', 'situacao_cadastral', 'cnae', 'natureza_juridica')
    list_display_links = ("cnpj", 'slug')
    list_per_page = 50
    list_filter = ('situacao_cadastral', 'natureza_juridica')
    search_fields = ('razao_social', 'nome_fantasia', 'cnae')
    readonly_fields = ("slug",)


admin.site.register(models.CompanyAccountModel, CompanyAccountAdmin)
