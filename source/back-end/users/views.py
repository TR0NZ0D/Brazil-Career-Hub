# pylint: disable=C0302
"""
users/views.py

Created by: Gabriel Menezes de Antonio
"""
from datetime import date
from typing import TypeAlias

import coreapi  # type: ignore
import coreschema  # type: ignore

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from api.tools.api_tools import description_generator
from api.tools.constants import (DEFAULT_COVER_COLOR, DEFAULT_PRIMARY_COLOR,
                                 DEFAULT_SECONDARY_COLOR, genders__str__,
                                 genders_keys, supported_languages__str__,
                                 supported_languages_keys)
from api.views import Base

from . import models, serializers

User = get_user_model()
user_model: TypeAlias = User  # type: ignore


# =================== User Profile =================== #
class UserProfileSchema(AutoSchema):
    """Schema for user profile"""

    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

Inform PK or slug if mentioning specific user profile, PK will prevail if both fields are sent

"""

        choices_info = f"""

## Supported languages

{supported_languages__str__}

## Available genders

{genders__str__}
"""
        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'User profile found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User profile not found'
                    }
                }
                return description_generator(title="Get a specific user profile.",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'User profile successfully created'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User account ID or badge ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create an user profile",
                                             description=authorization_info + choices_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'User profile successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User profile ID, user account ID or badge ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from user profile",
                                             # noqa: E502
                                             description=query_params_info + \
                                             authorization_info + choices_info,
                                             responses=responses)
            case 'PUT':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'User profile successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User profile ID, user account ID or badge ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update all data from user profile",
                                             # noqa: E502
                                             description=query_params_info + \
                                             authorization_info + choices_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'User profile successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User profile not found'
                    }
                }
                return description_generator(title="Delete a specific user profile",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case 'GET':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User profile ID"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(min_length=2),
                        description="User profile slug"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="user_username",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="User's account username"
                    ),
                    coreapi.Field(
                        name="language",
                        location='form',
                        required=True,
                        schema=coreschema.String(5),
                        description="Supported language key"
                    ),
                    coreapi.Field(
                        name="gender",
                        location='form',
                        required=True,
                        schema=coreschema.String(2),
                        description="Available gender key"
                    ),
                    coreapi.Field(
                        name="birth_date",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="User's birth date"
                    ),
                    coreapi.Field(
                        name="age",
                        location='form',
                        required=True,
                        schema=coreschema.Integer(),
                        description="User's age"
                    ),
                    coreapi.Field(
                        name="biography",
                        location='form',
                        required=False,
                        schema=coreschema.String(200),
                        description="User's profile biography"
                    ),
                    coreapi.Field(
                        name="company",
                        location='form',
                        required=False,
                        schema=coreschema.String(100),
                        description="User's company"
                    ),
                    coreapi.Field(
                        name="locale",
                        location='form',
                        required=False,
                        schema=coreschema.String(80),
                        description="User's locale"
                    ),
                    coreapi.Field(
                        name="website",
                        location='form',
                        required=False,
                        schema=coreschema.String(200),
                        description="User's website"
                    ),
                    coreapi.Field(
                        name="image",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="User's profile image"
                    ),
                    coreapi.Field(
                        name="email_confirmed",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="Is user's email confirmed"
                    ),
                    coreapi.Field(
                        name="recovery_key",
                        location='form',
                        required=False,
                        schema=coreschema.String(25),
                        description="Recovery key from user's account recovery process"
                    ),
                    coreapi.Field(
                        name="cover_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile cover color [HEX]"
                    ),
                    coreapi.Field(
                        name="primary_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile primary color [HEX]"
                    ),
                    coreapi.Field(
                        name="secondary_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile secondary color [HEX]"
                    ),
                    coreapi.Field(
                        name="banned",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="Is user banned"
                    ),
                    coreapi.Field(
                        name="reset_password",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="User must reset password on next login"
                    ),
                    coreapi.Field(
                        name="badges",
                        location='form',
                        required=False,
                        schema=coreschema.Array(items=coreschema.Integer(1)),
                        description="Array of badges IDs that this user has"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User profile ID"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(min_length=2),
                        description="User profile slug"
                    ), coreapi.Field(
                        name="user_username",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="User's account username"
                    ),
                    coreapi.Field(
                        name="language",
                        location='form',
                        required=True,
                        schema=coreschema.String(5),
                        description="Supported language key"
                    ),
                    coreapi.Field(
                        name="gender",
                        location='form',
                        required=True,
                        schema=coreschema.String(2),
                        description="Available gender key"
                    ),
                    coreapi.Field(
                        name="birth_date",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="User's birth date"
                    ),
                    coreapi.Field(
                        name="age",
                        location='form',
                        required=True,
                        schema=coreschema.Integer(),
                        description="User's age"
                    ),
                    coreapi.Field(
                        name="biography",
                        location='form',
                        required=False,
                        schema=coreschema.String(200),
                        description="User's profile biography"
                    ),
                    coreapi.Field(
                        name="company",
                        location='form',
                        required=False,
                        schema=coreschema.String(100),
                        description="User's company"
                    ),
                    coreapi.Field(
                        name="locale",
                        location='form',
                        required=False,
                        schema=coreschema.String(80),
                        description="User's locale"
                    ),
                    coreapi.Field(
                        name="website",
                        location='form',
                        required=False,
                        schema=coreschema.String(200),
                        description="User's website"
                    ),
                    coreapi.Field(
                        name="image",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="User's profile image"
                    ),
                    coreapi.Field(
                        name="email_confirmed",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="Is user's email confirmed"
                    ),
                    coreapi.Field(
                        name="recovery_key",
                        location='form',
                        required=False,
                        schema=coreschema.String(25),
                        description="Recovery key from user's account recovery process"
                    ),
                    coreapi.Field(
                        name="cover_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile cover color [HEX]"
                    ),
                    coreapi.Field(
                        name="primary_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile primary color [HEX]"
                    ),
                    coreapi.Field(
                        name="secondary_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile secondary color [HEX]"
                    ),
                    coreapi.Field(
                        name="banned",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="Is user banned"
                    ),
                    coreapi.Field(
                        name="reset_password",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="User must reset password on next login"
                    ),
                    coreapi.Field(
                        name="badges",
                        location='form',
                        required=False,
                        schema=coreschema.Array(items=coreschema.Integer(1)),
                        description="Array of badges IDs that this user has"
                    )
                ]
            case 'PUT':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User profile ID"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(min_length=2),
                        description="User profile slug"
                    ), coreapi.Field(
                        name="user_username",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="User's account username"
                    ),
                    coreapi.Field(
                        name="language",
                        location='form',
                        required=True,
                        schema=coreschema.String(5),
                        description="Supported language key"
                    ),
                    coreapi.Field(
                        name="gender",
                        location='form',
                        required=True,
                        schema=coreschema.String(2),
                        description="Available gender key"
                    ),
                    coreapi.Field(
                        name="birth_date",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="User's birth date"
                    ),
                    coreapi.Field(
                        name="age",
                        location='form',
                        required=True,
                        schema=coreschema.Integer(),
                        description="User's age"
                    ),
                    coreapi.Field(
                        name="biography",
                        location='form',
                        required=False,
                        schema=coreschema.String(200),
                        description="User's profile biography"
                    ),
                    coreapi.Field(
                        name="company",
                        location='form',
                        required=False,
                        schema=coreschema.String(100),
                        description="User's company"
                    ),
                    coreapi.Field(
                        name="locale",
                        location='form',
                        required=False,
                        schema=coreschema.String(80),
                        description="User's locale"
                    ),
                    coreapi.Field(
                        name="website",
                        location='form',
                        required=False,
                        schema=coreschema.String(200),
                        description="User's website"
                    ),
                    coreapi.Field(
                        name="image",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="User's profile image"
                    ),
                    coreapi.Field(
                        name="email_confirmed",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="Is user's email confirmed"
                    ),
                    coreapi.Field(
                        name="recovery_key",
                        location='form',
                        required=False,
                        schema=coreschema.String(25),
                        description="Recovery key from user's account recovery process"
                    ),
                    coreapi.Field(
                        name="cover_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile cover color [HEX]"
                    ),
                    coreapi.Field(
                        name="primary_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile primary color [HEX]"
                    ),
                    coreapi.Field(
                        name="secondary_color",
                        location='form',
                        required=False,
                        schema=coreschema.String(7),
                        description="User's profile secondary color [HEX]"
                    ),
                    coreapi.Field(
                        name="banned",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="Is user banned"
                    ),
                    coreapi.Field(
                        name="reset_password",
                        location='form',
                        required=False,
                        schema=coreschema.Boolean(default=False),
                        description="User must reset password on next login"
                    ),
                    coreapi.Field(
                        name="badges",
                        location='form',
                        required=False,
                        schema=coreschema.Array(items=coreschema.Integer(1)),
                        description="Array of badges IDs that this user has"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User profile ID"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(min_length=2),
                        description="User profile slug"
                    )
                ]
            case _:
                return []


class UserProfile(Base):
    """Manage user profile"""

    not_found_id_str = "Profile ID not found"
    not_found_slug_str = "Profile slug not found"
    not_found_profile_str = "User profile not found"

    schema = UserProfileSchema()

    def handle_profile_data(self, request,
                            # noqa
                            bypass_required: bool = False) -> tuple[bool, dict[str, user_model | \
                                                                    str | int | list[int] | \
                                                                    bool | date | None] | \
                                                                    Response]:
        """Handle profile data"""
        def generate_error_response(text: str) -> tuple[bool, Response]:
            return (False, self.generate_basic_response(status.HTTP_400_BAD_REQUEST, text))

        # Required
        username: str = request.data.get('user_username', None)
        language: str = request.data.get('language', None)
        gender: str = request.data.get('gender', None)

        # Optionals
        birth_date: str = request.data.get('birth_date', None)
        age: int = request.data.get('age', None)
        biography: str = request.data.get('biography', None)
        company: str = request.data.get('company', None)
        locale: str = request.data.get('locale', None)
        website: str = request.data.get('website', None)
        image = request.FILES.get('image', None)
        email_confirmed: bool = request.data.get('email_confirmed', None)
        recovery_key: str = request.data.get('recovery_key', None)
        cover_color: str = request.data.get('cover_color', None)
        primary_color: str = request.data.get('primary_color', None)
        secondary_color: str = request.data.get('secondary_color', None)
        banned: bool = request.data.get('banned', None)
        must_reset_password: bool = request.data.get('reset_password', None)
        badges: list[int] = request.data.get('badges', None)
        formatted_birth_date: date | None = None

        # Username validations
        if not username and not bypass_required:
            return generate_error_response('User username is required')

        if not isinstance(username, str):
            return generate_error_response('User username must be a string')

        user: user_model | None = User.objects.all().filter(username=username).first()

        if user is None:
            return generate_error_response('This username does not exist')

        # Language validations
        if not language and not bypass_required:
            return generate_error_response('Language is required')

        if not isinstance(language, str):
            return generate_error_response('Language must be a string')

        if language not in supported_languages_keys:
            return generate_error_response(f'Language {language} is not supported')

        # Gender validations
        if not gender and not bypass_required:
            return generate_error_response('Gender is required')

        if not isinstance(gender, str):
            return generate_error_response('Gender must be a string')

        if gender not in genders_keys:
            return generate_error_response(f'Gender {gender} is not available')

        # Birth date validations
        if birth_date and not isinstance(birth_date, str):
            return generate_error_response('Birth date must be a string')

        if birth_date:
            try:
                formatted_birth_date = date.fromisoformat(birth_date)
            except ValueError:
                return generate_error_response('Birth date must follow the ISO \
                                                8601 date format (yyyy-mm-dd)')

        # Age validations
        if age:
            try:
                age = int(age)
            except ValueError:
                return generate_error_response('Age must be an integer')

        if age and age not in range(1, 125):
            return generate_error_response('Age must be in range 1...125')

        # Biography validations
        if biography and not isinstance(biography, str):
            return generate_error_response('Biography must be a string')

        if biography and len(biography) > 200:
            return generate_error_response('Biography must have a max length of 200 characters')

        # Company validations
        if company and not isinstance(company, str):
            return generate_error_response('Company must be a string')

        if company and len(company) > 100:
            return generate_error_response('Company must have a max length of 100 characters')

        # Locale validations
        if locale and not isinstance(locale, str):
            return generate_error_response('Locale must be a string')

        if locale and len(locale) > 80:
            return generate_error_response('Locale must have a max length of 80 characters')

        # Website validations
        if website and not isinstance(website, str):
            return generate_error_response('Website must be a string')

        if website and len(website) > 200:
            return generate_error_response('Website must have a max length of 200 characters')

        # Image validations
        # TODO: Review image validation
        if image:
            image = image  # pylint: disable=W0127

        # Email confirmed validations
        if email_confirmed:
            if 'true' in str(email_confirmed).lower():
                email_confirmed = True
            elif 'false' in str(email_confirmed).lower():
                email_confirmed = False
            else:
                return generate_error_response('Email confirmed must be a boolean')

        # Recovery key validations
        if recovery_key and not isinstance(recovery_key, str):
            return generate_error_response('Recovery key must be a string')

        if recovery_key and len(recovery_key) > 25:
            return generate_error_response('Recovery key must have a max length of 25 characters')

        # Cover color validations
        if cover_color and not isinstance(cover_color, str):
            return generate_error_response('Cover color must be a string')

        if cover_color and (not cover_color.startswith("#") or len(cover_color) != 7):
            return generate_error_response('Cover color must follow the HEX pattern: #000000')

        if cover_color == '':
            cover_color = DEFAULT_COVER_COLOR

        # Primary color validations
        if primary_color and not isinstance(primary_color, str):
            return generate_error_response('Primary color must be a string')

        if primary_color and (not primary_color.startswith("#") or len(primary_color) != 7):
            return generate_error_response('Primary color must follow the HEX pattern: #000000')

        if primary_color == '':
            primary_color = DEFAULT_PRIMARY_COLOR

        # Secondary color validations
        if secondary_color and not isinstance(secondary_color, str):
            return generate_error_response('Secondary color must be a string')

        if secondary_color and (not secondary_color.startswith("#") or len(secondary_color) != 7):
            return generate_error_response('Secondary color must follow the HEX pattern: #000000')

        if secondary_color == '':
            secondary_color = DEFAULT_SECONDARY_COLOR

        # Banned validations
        if banned:
            if 'true' in str(banned).lower():
                banned = True
            elif 'false' in str(banned).lower():
                banned = False
            else:
                return generate_error_response('Banned must be a boolean')

        # Must reset pass validations
        if must_reset_password:
            if 'true' in str(must_reset_password).lower():
                must_reset_password = True
            elif 'false' in str(must_reset_password).lower():
                must_reset_password = False
            else:
                return generate_error_response('Reset password must be a boolean')

        # Badges validations
        if badges and not isinstance(badges, list):
            return generate_error_response('Badges must be an array of integers')

        if badges:
            try:
                [isinstance(badge_id, int)
                 for badge_id in [int(badge) for badge in badges]]
            except ValueError:
                return generate_error_response('All items in badges array must be integers')

            unexisting_ids = {int(badge_id) if not models.UserBadges.objects.all()
                              .filter(pk=int(badge_id)).exists() else '' for badge_id in badges}

            if '' in unexisting_ids:
                unexisting_ids.remove('')

            if unexisting_ids:
                response_singular = f'Please remove the following badge ID \
                                    from array since it does not exist: {unexisting_ids}'
                response_plural = f'Please remove the following badges \
                                  IDs since they does not exist: {unexisting_ids}'
                return generate_error_response(response_plural if len(unexisting_ids) > 1
                                               else response_singular)

        # Data conversion and handling
        data: dict[str, user_model | str | int | list[int] | bool | date | None] = {
            'user': user,
            'language': language,
            'gender': gender,
            'birth_date': formatted_birth_date,
            'age': int(age),
            'biography': biography,
            'company': company,
            'locale': locale,
            'website': website,
            'image': image,
            'email_confirmed': email_confirmed,
            'recovery_key': recovery_key,
            'cover_color': cover_color,
            'primary_color': primary_color,
            'secondary_color': secondary_color,
            'banned': banned,
            'must_reset_password': must_reset_password,
            'badges': badges,
        }

        return (True, data)

    def get(self, request):
        """Get request"""
        primary_key = request.query_params.get('pk', None)

        if primary_key is None:
            slug = request.query_params.get('slug', None)

            if slug is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_nor_id_str)
            if not slug:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_str)

            user_profile = models.UserProfile.objects.all().filter(slug=slug).first()
        else:
            if not primary_key:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_id_str)

            user_profile = models.UserProfile.objects.all().filter(pk=primary_key).first()

        if user_profile is not None:
            serializer = serializers.UserProfileSerializer(user_profile)
            data = serializer.data
            try:
                # type: ignore
                data['image'] = f"/media{user_profile.image.path.split('/media')[1]}"
            except IndexError:
                data['image'] = None
            return Response(data=data, status=status.HTTP_200_OK)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_profile_str)

    def post(self, request):
        """Post request"""
        data_valid, data_or_response = self.handle_profile_data(request)
        if not data_valid:
            return data_or_response

        profile_data = data_or_response

        user = profile_data.get('user', None)

        if user is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'User not found')

        profile = models.UserProfile(user=user,
                                     age=profile_data.get(
                                         'age', 0),  # type: ignore
                                     birth_date=profile_data.get(
                                         'birth_date', date.today()),  # type: ignore
                                     biography=profile_data.get(
                                         'biography', ''),
                                     company=profile_data.get('company', ''),
                                     locale=profile_data.get('locale', ''),
                                     website=profile_data.get('website', ''),
                                     image=profile_data.get('image'),
                                     email_confirmed=profile_data.get(
                                         'email_confirmed', False),  # type: ignore
                                     recovery_key=profile_data.get(
                                         'recovery_key', ''),
                                     language=profile_data.get(
                                         'language', 'pt-br'),
                                     gender=profile_data.get('gender', 'NI'),
                                     cover_color=profile_data.get(
                                         'cover_color', DEFAULT_COVER_COLOR),
                                     primary_color=profile_data.get(
                                         'primary_color', DEFAULT_PRIMARY_COLOR),
                                     secondary_color=profile_data.get(
                                         'secondary_color', DEFAULT_SECONDARY_COLOR),
                                     banned=profile_data.get(
                                         'banned', False),  # type: ignore
                                     must_reset_password=profile_data.get(
                                         'must_reset_password', False)  # type: ignore
                                     )

        if profile_data.get('image', None):  # TODO: Image posting is not working
            profile.image = profile_data.get('image')  # type: ignore

        if profile_data.get('badges', None):
            for badge_id in profile_data.get('badges', []):  # type: ignore
                try:
                    badge = models.UserBadges.objects.get(pk=badge_id)
                    profile.badges.add(badge)
                except Exception:  # pylint: disable=W0718
                    continue

        data = serializers.UserProfileSerializer(profile, many=False).data
        serializer = serializers.UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            try:
                data['image'] = f"/media{profile.image.path.split('/media')[1]}"  # type: ignore
            except IndexError:
                data['image'] = None
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Patch request"""
        primary_key = request.query_params.get('pk', None)

        if primary_key is None:
            slug = request.query_params.get('slug', None)

            if slug is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_nor_id_str)
            if not slug:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_str)

            user_profile = models.UserProfile.objects.all().filter(slug=slug).first()
        else:
            if not primary_key:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_id_str)

            user_profile = models.UserProfile.objects.all().filter(pk=primary_key).first()

        if user_profile is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_profile_str)

        data_valid, data_or_response = self.handle_profile_data(
            request, bypass_required=True)
        if not data_valid:
            return data_or_response

        profile_data = data_or_response

        if profile_data.get('user', None):
            user: User = profile_data.get('user', None)  # type: ignore
            if user is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'User not found')
            user_profile.user = user

        if profile_data.get('language', None):
            language: str = profile_data.get('language', 'pt-br')  # type: ignore
            user_profile.language = language

        if profile_data.get('gender', None):
            gender: str = profile_data.get('gender', 'NI')  # type: ignore
            user_profile.gender = gender

        if profile_data.get('age', None):
            age: int = profile_data.get('age', 0)  # type: ignore
            user_profile.age = age

        if profile_data.get('birth_date', None):
            birth_date: date = profile_data.get('birth_date', date.today())  # type: ignore
            user_profile.birth_date = birth_date

        if profile_data.get('biography', None):
            bio: str = profile_data.get('biography', '')  # type: ignore
            user_profile.biography = bio

        if profile_data.get('company', None):
            company: str = profile_data.get('company', '')  # type: ignore
            user_profile.company = company

        if profile_data.get('locale', None):
            locale: str = profile_data.get('locale', '')  # type: ignore
            user_profile.locale = locale

        if profile_data.get('website', None):
            website: str = profile_data.get('website', '')  # type: ignore
            user_profile.website = website

        if profile_data.get('image', None):
            image = profile_data.get('image')  # type: ignore
            user_profile.image = image  # type: ignore

        if profile_data.get('email_confirmed', None):
            email_confirmed: bool = profile_data.get('email_confirmed', False)  # type: ignore
            user_profile.email_confirmed = email_confirmed

        if profile_data.get('recovery_key', None):
            recovery_key: str = profile_data.get('recovery_key', '')  # type: ignore
            user_profile.recovery_key = recovery_key

        if profile_data.get('cover_color', None):
            cover_color: str = profile_data.get('cover_color', DEFAULT_COVER_COLOR)  # type: ignore
            user_profile.cover_color = cover_color

        if profile_data.get('primary_color', None):
            primary_color: str = profile_data.get('primary_color',  # type: ignore
                                                  DEFAULT_PRIMARY_COLOR)  # type: ignore
            user_profile.primary_color = primary_color

        if profile_data.get('secondary_color', None):
            secondary_color: str = profile_data.get('secondary_color',  # type: ignore
                                                    DEFAULT_SECONDARY_COLOR)  # type: ignore
            user_profile.secondary_color = secondary_color

        if profile_data.get('banned', None):
            banned: bool = profile_data.get('banned', False)  # type: ignore
            user_profile.banned = banned

        if profile_data.get('must_reset_password', None):
            must_reset_pass: bool = profile_data.get('must_reset_password', False)  # type: ignore
            user_profile.must_reset_password = must_reset_pass

        try:
            user_profile.clean_fields()
            user_profile.clean()
        except ValidationError as err:
            data = self.generate_basic_response_data(
                status.HTTP_400_BAD_REQUEST, 'Patch data validation error')
            data['errors'] = err
            return Response(data=data, status=data.get('status'))

        user_profile.save()

        serializer = serializers.UserProfileSerializer(user_profile)
        data = serializer.data
        try:
            data['image'] = f"/media{user_profile.image.path.split('/media')[1]}"  # type: ignore
        except IndexError:
            data['image'] = None

        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request):
        """Put request"""
        primary_key = request.query_params.get('pk', None)

        if primary_key is None:
            slug = request.query_params.get('slug', None)

            if slug is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_nor_id_str)
            if not slug:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_str)

            user_profile = models.UserProfile.objects.all().filter(slug=slug).first()
        else:
            if not primary_key:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_id_str)

            user_profile = models.UserProfile.objects.all().filter(pk=primary_key).first()

        if user_profile is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_profile_str)

        data_valid, data_or_response = self.handle_profile_data(request)
        if not data_valid:
            return data_or_response

        profile_data = data_or_response

        user = profile_data.get('user', None)

        if user is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'User not found')

        profile = models.UserProfile(user=user,
                                     age=profile_data.get('age', 0),  # type: ignore
                                     birth_date=profile_data.get('birth_date',  # type: ignore
                                                                 date.today()),  # type: ignore
                                     biography=profile_data.get('biography', ''),
                                     company=profile_data.get('company', ''),
                                     locale=profile_data.get('locale', ''),
                                     website=profile_data.get('website', ''),
                                     email_confirmed=profile_data.get(
                                         'email_confirmed', False),  # type: ignore
                                     recovery_key=profile_data.get(
                                         'recovery_key', ''),
                                     language=profile_data.get(
                                         'language', 'pt-br'),
                                     gender=profile_data.get('gender', 'NI'),
                                     cover_color=profile_data.get(
                                         'cover_color', DEFAULT_COVER_COLOR),
                                     primary_color=profile_data.get(
                                         'primary_color', DEFAULT_PRIMARY_COLOR),
                                     secondary_color=profile_data.get(
                                         'secondary_color', DEFAULT_SECONDARY_COLOR),
                                     banned=profile_data.get(
                                         'banned', False),  # type: ignore
                                     must_reset_password=profile_data.get(
                                         'must_reset_password', False)  # type: ignore
                                     )

        if profile_data.get('image', None):
            profile.image = profile_data.get('image')  # type: ignore

        if profile_data.get('badges', None):
            for badge_id in profile_data.get('badges', []):  # type: ignore
                try:
                    badge = models.UserBadges.objects.get(pk=badge_id)
                    profile.badges.add(badge)
                except Exception:  # pylint: disable=W0718
                    continue

        data = serializers.UserProfileSerializer(profile, many=False).data
        serializer = serializers.UserProfileSerializer(user_profile, data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            try:
                # type: ignore
                data['image'] = f"/media{user_profile.image.path.split('/media')[1]}"
            except IndexError:
                data['image'] = None
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete request"""
        primary_key = request.query_params.get('pk', None)

        if primary_key is None:
            slug = request.query_params.get('slug', None)

            if slug is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_nor_id_str)
            if not slug:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_slug_str)

            user_profile = models.UserProfile.objects.all().filter(slug=slug).first()
        else:
            if not primary_key:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_id_str)

            user_profile = models.UserProfile.objects.all().filter(pk=primary_key).first()

        if user_profile is not None:
            user_profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_profile_str)


# =================== Badges =================== #
class BadgesSchema(AutoSchema):
    """Schema for badges"""

    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""
        query_params_info = """
## Query Parameters

Inform PK if mentioning specific badge.

"""
        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Badge found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Bagde not found'
                    }
                }
                return description_generator(title="Get all badges or a specific one",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Badge successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Creates a badge",
                                             description=authorization_info,
                                             responses=responses)
            case 'PUT':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Badge updated successfully'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Badge ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Updates all data from a specific badge",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Badge successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Badge ID not found'
                    }
                }
                return description_generator(title="Deletes a badge",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case 'GET':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Badge ID"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="name",
                        location="form",
                        required=True,
                        schema=coreschema.String(20),
                        description="Badge name"
                    ), coreapi.Field(
                        name="description",
                        location='form',
                        required=True,
                        schema=coreschema.String(255),
                        description="Badge description"
                    ), coreapi.Field(
                        name="color",
                        location='form',
                        required=True,
                        schema=coreschema.String(7, format='#{0:06x}'),
                        description="Badge color [HEX]"
                    )
                ]
            case 'PUT':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Badge ID"
                    ),
                    coreapi.Field(
                        name="name",
                        location="form",
                        required=True,
                        schema=coreschema.String(20),
                        description="Badge name"
                    ), coreapi.Field(
                        name="description",
                        location='form',
                        required=True,
                        schema=coreschema.String(255),
                        description="Badge description"
                    ), coreapi.Field(
                        name="color",
                        location='form',
                        required=True,
                        schema=coreschema.String(7, format='#{0:06x}'),
                        description="Badge color [HEX]"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Badge ID"
                    )
                ]
            case _:
                return []


class UserBadges(Base):
    """Manage user badges"""

    not_found_id_str = "Badge ID not found"

    schema = BadgesSchema()

    def get(self, request):
        """Get request"""
        primary_key = request.query_params.get('pk', None)

        if (not primary_key) and (primary_key is not None):
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        if primary_key is None:
            user_badges = models.UserBadges.objects.all()
            serializer = serializers.UserBadgesSerializer(
                user_badges, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        user_badge = models.UserBadges.objects.all().filter(pk=primary_key).first()
        if user_badge is not None:
            serializer = serializers.UserBadgesSerializer(user_badge)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

    def post(self, request):
        """Post request"""
        name = request.data.get('name', None)
        description = request.data.get('description', None)
        color = request.data.get('color', None)
        badge = models.UserBadges(
            name=name, description=description, color=color)
        data = serializers.UserBadgesSerializer(badge, many=False).data

        serializer = serializers.UserBadgesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Put request"""
        primary_key = request.query_params.get('pk', None)

        if not primary_key:
            primary_key = request.data.get('pk', None)

        if not primary_key:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        user_badge = models.UserBadges.objects.all().filter(pk=primary_key).first()
        if user_badge is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        name = request.data.get('name', user_badge.name)
        description = request.data.get('description', user_badge.description)
        color = request.data.get('color', user_badge.color)
        badge = models.UserBadges(
            name=name, description=description, color=color)
        data = serializers.UserBadgesSerializer(badge, many=False).data
        serializer = serializers.UserBadgesSerializer(user_badge, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete request"""
        primary_key = request.query_params.get('pk', None)

        if not primary_key:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        user_badge = models.UserBadges.objects.all().filter(pk=primary_key).first()
        if user_badge is not None:
            user_badge.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)


# =================== Banned Users =================== #
class BannedUsersSchema(AutoSchema):
    """Schema for banned users"""

    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""
        query_params_info = """
## Query Parameters

Inform PK or slug if mentioning specific issue, PK will prevail if both fields are sent

"""
        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Ban issue was found.'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Ban issue not found'
                    }
                }
                return description_generator(title="Lists all ban issues or gets a specific issue.",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Ban issue created successfully'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User, profile or responsible not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Creates a ban issue for the mentioned user",
                                             description=authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Ban issue was successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Ban issue not found'
                    }
                }
                return description_generator(title="Delete the mentioned ban issue",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case 'GET':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Ban issue ID"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(min_length=2),
                        description="Banned user profile slug"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="user_username",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="Banned user's username"
                    ), coreapi.Field(
                        name="profile_slug",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Banned user's profile slug"
                    ), coreapi.Field(
                        name="reason",
                        location='form',
                        required=True,
                        schema=coreschema.String(2000),
                        description="Ban reason"
                    ), coreapi.Field(
                        name="responsible_username",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Username of the admin responsible for creating the ban issue"
                    ), coreapi.Field(
                        name="ip",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Banned user's IP"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Ban issue ID"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(min_length=2),
                        description="Banned user profile slug"
                    )
                ]
            case _:
                return []


class BannedUsers(Base):
    """Manage banned users issues"""

    not_found_id_str = "Ban ID not found"
    not_found_slug_str = "User slug not found"
    not_found_slug_nor_id_str = "Neither ID nor slug found"
    slug_not_banned_str = "User with given slug is not banned"

    schema = BannedUsersSchema()

    def get(self, request):
        """Get request"""
        primary_key = request.query_params.get('pk', None)

        slug = request.query_params.get('slug', None)

        if (not primary_key) and (primary_key is not None):
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        if (not slug) and (slug is not None):
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_slug_str)

        if primary_key:
            banned_user = models.BannedUsers.objects.all().filter(pk=primary_key).first()
            if banned_user is not None:
                serializer = serializers.BannedUsersSerializer(banned_user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        if slug:
            banned_user = models.BannedUsers.objects.all().filter(profile__slug=slug).first()
            if banned_user is not None:
                serializer = serializers.BannedUsersSerializer(banned_user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.slug_not_banned_str)

        banned_users = models.BannedUsers.objects.all()
        serializer = serializers.BannedUsersSerializer(
            banned_users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Post request"""
        user_username = request.data.get('user_username', None)
        user = User.objects.all().filter(username=user_username).first()
        profile_slug = request.data.get('profile_slug', None)
        profile = models.UserProfile.objects.all().filter(slug=profile_slug).first()
        reason = request.data.get('reason', None)
        responsible_username = request.data.get('responsible_username', None)
        responsible = User.objects.all().filter(username=responsible_username).first()
        user_ip = request.data.get('ip', None)

        if user is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                "Banned user username not found")

        if profile is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                "Banned user profile slug not found")

        if responsible is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                "Admin responsible username not found")

        ban_issue = models.BannedUsers(
            user=user, profile=profile, reason=reason, responsible=responsible, ip=user_ip)
        data = serializers.BannedUsersSerializer(ban_issue).data
        serializer = serializers.BannedUsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete request"""
        primary_key = request.query_params.get('pk', None)

        slug = request.query_params.get('slug', None)

        if (not primary_key) and (primary_key is not None):
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        if (not slug) and (slug is not None):
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_slug_str)

        if primary_key:
            banned_user = models.BannedUsers.objects.all().filter(pk=primary_key).first()
            if banned_user is not None:
                banned_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        if slug:
            banned_user = models.BannedUsers.objects.all().filter(profile__slug=slug).first()
            if banned_user is not None:
                banned_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.slug_not_banned_str)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_slug_nor_id_str)
