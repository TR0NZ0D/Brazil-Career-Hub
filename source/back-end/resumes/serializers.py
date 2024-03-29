from rest_framework import serializers

from . import models


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeExperience
        fields = '__all__'


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeCompetence
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeCourse
        fields = '__all__'


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeReference
        fields = '__all__'


class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeGraduation
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeProject
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResumeLink
        fields = '__all__'


class ResumeModelSerializer(serializers.ModelSerializer):
    all_experiences = serializers.SerializerMethodField()
    all_competencies = serializers.SerializerMethodField()
    all_courses = serializers.SerializerMethodField()
    all_references = serializers.SerializerMethodField()
    all_graduations = serializers.SerializerMethodField()
    all_projects = serializers.SerializerMethodField()
    all_links = serializers.SerializerMethodField()

    def get_all_experiences(self, obj):
        return obj.experiences.all().values()

    def get_all_competencies(self, obj):
        return obj.competencies.all().values()

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
                  "all_competencies",
                  "all_courses",
                  "all_references",
                  "all_graduations",
                  "all_projects",
                  "all_links"
                  ]
