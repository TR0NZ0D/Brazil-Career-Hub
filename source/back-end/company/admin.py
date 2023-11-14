"""
company/admin.py

Created by: Gabriel Menezes de Antonio
"""

from django.contrib import admin

from . import models


class CompanyAccountAdmin(admin.ModelAdmin):
    """Admin model for company account"""
    list_display = ("pk", "cnpj", 'slug', 'registration_status', 'cnae', 'legal_nature', "deactivated",
                    "should_change_password", "banned")
    list_display_links = ("pk", "cnpj", 'slug')
    list_per_page = 50
    list_filter = ('registration_status', 'legal_nature', "deactivated", "should_change_password", "banned")
    search_fields = ('corporate_name', 'fantasy_name', 'cnae')
    readonly_fields = ("slug",)


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ("pk", "company_account", "creation_date", "financial_capital", "employees", "site_url")
    list_display_links = ("pk", "company_account")
    list_per_page = 50
    list_filter = ("creation_date",)
    search_fields = ("company_account", "address", "site_url")


class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "address", "number")
    list_display_links = ("pk", "title")
    list_per_page = 50
    search_fields = ("address", "titles")


class CompanySocialMediaAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "url", "username")
    list_display_links = ("pk", "title")
    list_per_page = 50
    search_fields = ("url", "title", "username")


admin.site.register(models.CompanyProfileModel, CompanyProfileAdmin)
admin.site.register(models.CompanyAddress, CompanyAddressAdmin)
admin.site.register(models.CompanySocialMedia, CompanySocialMediaAdmin)
admin.site.register(models.CompanyAccountModel, CompanyAccountAdmin)
