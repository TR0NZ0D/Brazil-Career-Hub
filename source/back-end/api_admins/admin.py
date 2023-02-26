from django.contrib import admin
from . import models


class ApiAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    list_display_links = ('user',)
    search_fields = ('user', 'token')
    readonly_fields = ('token',)
    list_per_page = 20


admin.site.register(models.ApiAdmin, ApiAdminAdmin)
