
from rest_framework import serializers

from . import models


class VacancyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VacancyModel
        fields = '__all__'
