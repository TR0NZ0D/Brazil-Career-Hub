"""
users/serializers.py

Created by: Gabriel Menezes de Antonio
"""
from rest_framework import serializers

from . import models


class CompanyAccountSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""

    registration_status_display = serializers.CharField(source="get_registration_status_display")
    legal_nature_display = serializers.CharField(source="get_legal_nature_display")

    class Meta:
        """Meta data for user profile serializer"""
        model = models.CompanyAccountModel
        fields = ['id', 'cnpj', 'corporate_name', 'registration_status_display', 'fantasy_name',
                  'cnae', 'legal_nature_display', 'slug']
