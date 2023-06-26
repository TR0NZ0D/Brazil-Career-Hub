"""
users/serializers.py

Created by: Gabriel Menezes de Antonio
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from . import models


class BannedUsersSerializer(serializers.ModelSerializer):
    """Serializer for banned users"""
    user_username = serializers.SerializerMethodField()
    profile_name = serializers.SerializerMethodField()
    responsible_username = serializers.SerializerMethodField()

    def get_user_username(self, obj) -> str:
        """Get user username string"""
        return obj.user.get_username()

    def get_profile_name(self, obj) -> str:
        """Get profile name string"""
        return str(obj.profile)

    def get_responsible_username(self, obj) -> str:
        """Get responsible username"""
        return obj.responsible.get_username()

    class Meta:
        """Meta data for banned users serializer"""
        model = models.BannedUsers
        fields = ['id', 'user', 'user_username', 'profile', 'profile_name',
                  'reason', 'responsible', 'responsible_username', 'date', 'ip']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""

    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    language_display = serializers.CharField(source="get_language_display")
    gender_display = serializers.CharField(source="get_gender_display")

    def get_username(self, obj) -> str:
        """Get user username string"""
        return obj.user.get_username()

    def get_email(self, obj) -> str:
        """Get user email"""
        return obj.user.email

    def get_first_name(self, obj) -> str:
        """Get user name"""
        return obj.user.first_name

    def get_last_name(self, obj) -> str:
        """Get user surname"""
        return obj.user.last_name

    class Meta:
        """Meta data for user profile serializer"""
        model = models.UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tag', 'age', 'birth_date',
                  'biography', 'company', 'locale', 'website', 'email_confirmed', 'slug',
                  'recovery_key', 'language_display', 'gender_display', 'cover_color',
                  'primary_color', 'secondary_color', 'banned', 'cpf', 'must_reset_password',
                  'nationality', 'phone_number', 'twitter_username', 'facebook_username',
                  'linkedin_username', 'instagram_username']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user account"""

    class Meta:
        """Meta data for user profile serializer"""
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
