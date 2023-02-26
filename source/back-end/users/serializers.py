"""
users/serializers.py

Created by: Gabriel Menezes de Antonio
"""
from rest_framework import serializers

from . import models


class UserBadgesSerializer(serializers.ModelSerializer):
    """Serializer for user badges"""
    class Meta:
        """Meta data for user bagdes serializer"""
        model = models.UserBadges
        fields = ['id', 'name', 'description', 'color']


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
    badges: serializers.StringRelatedField = serializers.StringRelatedField(
        many=True)

    class Meta:
        """Meta data for user profile serializer"""
        model = models.UserProfile
        fields = ['id', 'user', 'tag', 'age', 'birth_date',
                  'biography', 'company', 'locale', 'website',
                  'email_confirmed', 'slug', 'recovery_key',
                  'language', 'gender', 'cover_color', 'primary_color',
                  'secondary_color', 'banned', 'must_reset_password', 'badges']
