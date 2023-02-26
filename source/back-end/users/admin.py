from django.contrib import admin
from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('tag', 'user', 'slug', 'age', 'banned', 'must_reset_password')
    list_display_links = ('tag', 'user')
    list_per_page = 35
    list_filter = ('banned', 'must_reset_password', 'language', 'gender')
    search_fields = ('user', 'biography', 'company', 'locale', 'website')
    readonly_fields = ('tag', 'slug', 'recovery_key')


class BadgesInlineProfile(admin.StackedInline):
    model = models.UserProfile.badges.through
    extra = 0
    verbose_name = "Profile"
    verbose_name_plural = "Profiles"


class BadgesAdmin(admin.ModelAdmin):
    inlines = [BadgesInlineProfile]
    list_display = ('pk', 'name', 'color')
    list_display_links = ('pk', 'name')
    list_per_page = 20
    search_fields = ('name', 'description', 'color')


class BannedUsersAdmin(admin.ModelAdmin):
    list_display = ("pk", 'user', 'profile', 'responsible', 'date')
    list_display_links = ('pk', 'user')
    list_per_page = 25
    list_filter = ('date', 'responsible')
    search_fields = ('reason', 'ip', 'user', 'profile')
    readonly_fields = ("date",)


admin.site.register(models.UserProfile, ProfileAdmin)
admin.site.register(models.UserBadges, BadgesAdmin)
admin.site.register(models.BannedUsers, BannedUsersAdmin)
