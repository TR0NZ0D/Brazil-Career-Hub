from rest_framework import serializers

from . import models


class VacancyModelSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()

    def get_addresses(self, obj):
        if obj.address:
            return obj.address.__getattribute__("serialize")

        return []

    class Meta:
        model = models.VacancyModel
        fields = ["pk", "created_by", "role", "description", "modality", "created_at", "salary", "addresses", "resumes"]
