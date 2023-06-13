"""
users/admin.py

Created by: Gabriel Menezes de Antonio
"""
from django.contrib import admin

from . import models


class ProfileAdmin(admin.ModelAdmin):
    """Admin model for profile"""
    list_display = ('tag', 'user', 'slug', 'age', 'banned', 'must_reset_password')
    list_display_links = ('tag', 'user')
    list_per_page = 35
    list_filter = ('banned', 'must_reset_password', 'language', 'gender')
    search_fields = ('slug', 'biography', 'company', 'locale', 'website')
    readonly_fields = ('tag', 'slug', 'recovery_key')


class BannedUsersAdmin(admin.ModelAdmin):
    """Admin model for banned users"""
    list_display = ("pk", 'user', 'profile', 'responsible', 'date')
    list_display_links = ('pk', 'user')
    list_per_page = 25
    list_filter = ('date', 'responsible')
    search_fields = ('reason', 'ip', 'user', 'profile')
    readonly_fields = ("date",)


admin.site.register(models.UserProfile, ProfileAdmin)
admin.site.register(models.BannedUsers, BannedUsersAdmin)
