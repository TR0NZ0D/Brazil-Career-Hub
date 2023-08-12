from django.contrib import admin
from . import models


class ResumeExperiencesAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "experience_company",
                    "experience_role", 'experience_start_time',
                    'experience_end_time')
    list_display_links = ("pk", "profile")
    list_per_page = 50
    list_filter = ('experience_start_time', 'experience_end_time')
    search_fields = ('description', 'experience_company',
                     'experience_role', 'experience_description')


class ResumeCompetencesAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "competency_name", "competency_level")
    list_display_links = ("pk", "profile")
    list_per_page = 50
    search_fields = ('description', "competency_name", "competency_level")


class ResumeCoursesAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "course_name", "course_locale",
                    "course_provider", "course_hours", "course_start_time", "course_end_time")
    list_display_links = ("pk", "profile")
    list_per_page = 50
    list_filter = ("course_start_time", "course_end_time")
    search_fields = ('description', "course_name", "course_locale",
                     "course_provider", "course_hours")


class ResumeReferencesAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "reference_name", "reference_role",
                    "reference_company", "reference_phone", "refecence_email")
    list_display_links = ("pk", "profile")
    list_per_page = 50
    search_fields = ('description', "reference_name", "reference_role",
                     "reference_company", "reference_phone", "refecence_email")


class ResumeGraduationAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "graduation_type", "graduation_period", "graduation_start_time", "graduation_end_time")
    list_display_links = ("pk", "profile")
    list_per_page = 50
    list_filter = ("graduation_start_time", "graduation_end_time")
    search_fields = ('description', "graduation_type", "graduation_period")


class ResumeProjectsAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "project_name", "project_description", "project_link")
    list_display_links = ("pk", "profile")
    list_per_page = 50
    search_fields = ('description', "project_name", "project_description", "project_link")


class ResumeLinkAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "url")
    list_display_links = ("pk", "profile")
    list_per_page = 50
    search_fields = ('description', "url")


class ResumeModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "profile", "title", "created_at")
    list_display_links = ("pk", "profile")
    list_per_page = 50
    list_filter = ('created_at',)
    search_fields = ('description',)
    readonly_fields = ("created_at",)


admin.site.register(models.ResumeExperience, ResumeExperiencesAdmin)
admin.site.register(models.ResumeCompetence, ResumeCompetencesAdmin)
admin.site.register(models.ResumeCourse, ResumeCoursesAdmin)
admin.site.register(models.ResumeReference, ResumeReferencesAdmin)
admin.site.register(models.ResumeGraduation, ResumeGraduationAdmin)
admin.site.register(models.ResumeProject, ResumeProjectsAdmin)
admin.site.register(models.ResumeLink, ResumeLinkAdmin)
admin.site.register(models.ResumeModel, ResumeModelAdmin)
