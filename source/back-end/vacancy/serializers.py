from rest_framework import serializers

from . import models


class VacancyModelSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    def get_addresses(self, obj):
        if obj.address:
            return obj.address.__getattribute__("serialize")

        return []

    def get_company_name(self, obj: models.VacancyModel):
        return obj.created_by.fantasy_name

    class Meta:
        model = models.VacancyModel
        fields = ["pk", "created_by", "company_name", "role", "description", "modality", "created_at", "salary",
                  "addresses", "resumes"]
