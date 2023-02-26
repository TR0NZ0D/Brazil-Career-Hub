from rest_framework import serializers
from . import models


class UserBadgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserBadges
        fields = ['id', 'name', 'description', 'color']


class BannedUsersSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField()
    profile_name = serializers.SerializerMethodField()
    responsible_username = serializers.SerializerMethodField()

    def get_user_username(self, obj):
        return obj.user.get_username()

    def get_profile_name(self, obj):
        return str(obj.profile)

    def get_responsible_username(self, obj):
        return obj.responsible.get_username()

    class Meta:
        model = models.BannedUsers
        fields = ['id', 'user', 'user_username', 'profile', 'profile_name', 'reason', 'responsible', 'responsible_username', 'date', 'ip']


class UserProfileSerializer(serializers.ModelSerializer):
    badges: serializers.StringRelatedField = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.UserProfile
        fields = ['id', 'user', 'tag', 'age', 'birth_date',
                  'biography', 'company', 'locale', 'website',
                  'email_confirmed', 'slug', 'recovery_key',
                  'language', 'gender', 'cover_color', 'primary_color',
                  'secondary_color', 'banned', 'must_reset_password', 'badges']
