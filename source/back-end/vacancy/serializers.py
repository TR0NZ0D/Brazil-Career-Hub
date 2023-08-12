
from rest_framework import serializers

from . import models


class VacancyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VacancyAddress
        fields = '__all__'


class VacancyModelSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()

    def get_addresses(self, obj):
        return obj.address.__getattribute__("serialize")

    class Meta:
        model = models.VacancyModel
        fields = ["pk", "role", "description", "modality", "created_at", "salary", "addresses"]
