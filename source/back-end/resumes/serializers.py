from rest_framework import serializers

from . import models


class ResumeModelSerializer(serializers.ModelSerializer):
    all_experiences = serializers.ModelSerializer()
    all_competences = serializers.ModelSerializer()
    all_courses = serializers.ModelSerializer()
    all_references = serializers.ModelSerializer()
    all_graduations = serializers.ModelSerializer()
    all_projects = serializers.ModelSerializer()
    all_links = serializers.ModelSerializer()

    def get_all_experiences(self, obj):
        return obj.experiences.all().values()

    def get_all_competences(self, obj):
        return obj.competences.all().values()

    def get_all_courses(self, obj):
        return obj.courses.all().values()

    def get_all_references(self, obj):
        return obj.references.all().values()

    def get_all_graduations(self, obj):
        return obj.graduations.all().values()

    def get_all_projects(self, obj):
        return obj.projects.all().values()

    def get_all_links(self, obj):
        return obj.links.all().values()

    class Meta:
        model = models.ResumeModel
        fields = ["pk",
                  "profile",
                  'title',
                  "created_at",
                  "description",
                  "all_experiences",
                  "all_competences",
                  "all_courses",
                  "all_references",
                  "all_graduations",
                  "all_projects",
                  "all_links"
                  ]