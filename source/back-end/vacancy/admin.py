from django.contrib import admin
from . import models


class VacancyAddressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'address', 'number')
    list_display_links = ('pk', 'title')
    list_per_page = 35
    search_fields = ('title', 'address')


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'role', 'description', 'modality', 'created_at', 'salary')
    list_display_links = ('pk', 'role')
    list_per_page = 35
    list_filter = ('created_at',)
    search_fields = ('role', 'description', 'modality')
    readonly_fields = ('created_at',)


admin.site.register(models.VacancyAddress, VacancyAddressAdmin)
admin.site.register(models.VacancyModel, VacancyAdmin)
