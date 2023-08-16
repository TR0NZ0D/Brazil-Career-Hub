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
        fields = ['id', 'cnpj', "password", "deactivated", "should_change_password", "banned", 'corporate_name',
                  'registration_status_display', 'fantasy_name', 'cnae', 'legal_nature_display', 'slug']


class CreateCompanyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyAccountModel
        fields = "__all__"


class CompanyProfileSerializer(serializers.ModelSerializer):

    addresses = serializers.SerializerMethodField()
    social_medias = serializers.SerializerMethodField()
    cnpj = serializers.SerializerMethodField()
    corporate_name = serializers.SerializerMethodField()
    registration_status_display = serializers.SerializerMethodField()
    fantasy_name = serializers.SerializerMethodField()
    cnae = serializers.SerializerMethodField()
    legal_nature_display = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    deactivated = serializers.SerializerMethodField()
    should_change_password = serializers.SerializerMethodField()
    banned = serializers.SerializerMethodField()

    def get_password(self, obj):
        return obj.company_account.password

    def get_deactivated(self, obj):
        return obj.company_account.deactivated

    def get_should_change_password(self, obj):
        return obj.company_account.should_change_password

    def get_banned(self, obj):
        return obj.company_account.banned

    def get_addresses(self, obj):
        return obj.address.all().values()

    def get_social_medias(self, obj):
        return obj.social_media.all().values()

    def get_cnpj(self, obj):
        return obj.company_account.cnpj

    def get_corporate_name(self, obj):
        return obj.company_account.corporate_name

    def get_registration_status_display(self, obj):
        return obj.company_account.get_registration_status_display()

    def get_fantasy_name(self, obj):
        return obj.company_account.fantasy_name

    def get_cnae(self, obj):
        return obj.company_account.cnae

    def get_legal_nature_display(self, obj):
        return obj.company_account.get_legal_nature_display()

    def get_slug(self, obj):
        return obj.company_account.slug

    class Meta:
        model = models.CompanyProfileModel
        fields = ['cnpj', 'corporate_name', 'registration_status_display', 'fantasy_name',
                  'cnae', 'legal_nature_display', 'slug', "id", "company_account", "addresses",
                  "contact", "creation_date", "financial_capital", "employees", "site_url", "social_medias",
                  "password", "deactivated", "should_change_password", "banned"]


class CreateCompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyProfileModel
        fields = "__all__"
