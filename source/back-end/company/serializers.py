"""
users/serializers.py

Created by: Gabriel Menezes de Antonio
"""
from rest_framework import serializers

from . import models


class CompanyAccountSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""

    class Meta:
        """Meta data for user profile serializer"""
        model = models.CompanyAccountModel
        fields = ['id', 'cnpj', 'razao_social', 'situacao_cadastral', 'nome_fantasia',
                  'cnae', 'natureza_juridica', 'slug']
