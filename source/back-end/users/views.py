# pylint: disable=C0302
"""
users/views.py

Created by: Gabriel Menezes de Antonio
"""
from datetime import date
from typing import TypeAlias

import coreapi  # type: ignore
import coreschema  # type: ignore

from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from api.tools.api_tools import description_generator
from api.tools.constants import (DEFAULT_COVER_COLOR, DEFAULT_PRIMARY_COLOR,
                                 DEFAULT_SECONDARY_COLOR, genders__str__,
                                 genders_keys)
from api.views import Base

from . import models, serializers

User = get_user_model()
user_model: TypeAlias = User  # type: ignore


# =================== User Authentication =================== #
class UserAuthenticationSchema(AutoSchema):
    """Schema for user authentication"""

    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""
        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'User logged out successfully'
                    },
                    "500": {
                        'description': 'INTERNAL SERVER ERROR',
                        'reason': 'Something went wrong'
                    }
                }
                return description_generator(title="logout an user",
                                             description=authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'User authenticated and logged in successfully'
                    },
                    "202": {
                        'description': 'ACCEPTED',
                        'reason': 'User authenticated successfully, but, need to change password'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    },
                    "403": {
                        'description': 'FORBIDDEN',
                        'reason': 'Authentication failed'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User account not found'
                    },
                    "423": {
                        'description': 'LOCKED',
                        'reason': 'User account can\'t be accessed due to a ban or other issue'
                    },
                    "500": {
                        'description': 'INTERNAL SERVER ERROR',
                        'reason': 'Something went wrong'
                    }
                }
                return description_generator(title="Authenticate and login an user",
                                             description=authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case 'POST':
                return [
                    coreapi.Field(
                        name="username",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="User's account username"
                    ),
                    coreapi.Field(
                        name="password",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="User's account password"
                    )
                ]
            case _:
                return []


class UserAuthentication(Base):
    """Authenticate user"""

    schema = UserAuthenticationSchema()

    def get(self, request):
        """Get request"""

        return self.generate_basic_response(status.HTTP_200_OK, "Logged out")

    def post(self, request):
        """Post request"""
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                "Username or password not found")

        if request.user.is_authenticated:
            return self.generate_basic_response(status.HTTP_409_CONFLICT,
                                                "An user is already logged in")

        user = User.objects.all().filter(username=username).first()

        if user is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                "No account found with this username")

        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is None:
            return self.generate_basic_response(status.HTTP_403_FORBIDDEN,
                                                "Authentication failed, check your credentials")

        profile = models.UserProfile.objects.all().filter(user=authenticated_user).first()

        if profile is None:
            return self.generate_basic_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                "User profile not found")

        if profile.banned:
            return self.generate_basic_response(status.HTTP_423_LOCKED,
                                                "User's account is banned")

        if profile.must_reset_password:
            data = self.generate_basic_response_data(status.HTTP_202_ACCEPTED,
                                                     "User must change password before logging in")
            serializer = serializers.UserProfileSerializer(profile)
            data['content'] = serializer.data
            return Response(data=data, status=data.get('status', status.HTTP_202_ACCEPTED))

        data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                 "Logged in successfully")
        serializer = serializers.UserProfileSerializer(profile)
        data['content'] = serializer.data
        return Response(data=data, status=data.get('status', status.HTTP_200_OK))


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
                        'reason': 'User account ID not found'
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
                        'reason': 'User profile ID or user account ID not found'
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
                        name="languages",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(500)),
                        description="The languages that the user speaks"
                    ),
                    coreapi.Field(
                        name="gender",
                        location='form',
                        required=False,
                        schema=coreschema.String(2),
                        description="Available gender key"
                    ),
                    coreapi.Field(
                        name="birth_date",
                        location='form',
                        required=False,
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
                        name='nationality',
                        location='form',
                        required=True,
                        schema=coreschema.String(80),
                        description="This is the user's nationality."
                    ),
                    coreapi.Field(
                        name='cpf',
                        location='form',
                        required=False,
                        schema=coreschema.String(11),
                        description="User's CPF"
                    ),
                    coreapi.Field(
                        name='phone_number',
                        location='form',
                        required=False,
                        schema=coreschema.String(30),
                        description="User's phone number"
                    ),
                    coreapi.Field(
                        name='twitter_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(15),
                        description="User's Twitter account username"
                    ),
                    coreapi.Field(
                        name='facebook_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(50),
                        description="User's Facebook account username"
                    ),
                    coreapi.Field(
                        name='linkedin_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(60),
                        description="User's LinkedIn account username"
                    ),
                    coreapi.Field(
                        name='instagram_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(30),
                        description="User's Instagram account username"
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
                        required=False,
                        schema=coreschema.String(),
                        description="User's account username (this is intented to replace the user from this profile, \
                        not to change its username)"
                    ),
                    coreapi.Field(
                        name="languages",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(500)),
                        description="The languages that the user speaks"
                    ),
                    coreapi.Field(
                        name="gender",
                        location='form',
                        required=False,
                        schema=coreschema.String(2),
                        description="Available gender key"
                    ),
                    coreapi.Field(
                        name="birth_date",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="User's birth date"
                    ),
                    coreapi.Field(
                        name="age",
                        location='form',
                        required=False,
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
                        name='nationality',
                        location='form',
                        required=False,
                        schema=coreschema.String(80),
                        description="This is the user's nationality."
                    ),
                    coreapi.Field(
                        name='cpf',
                        location='form',
                        required=False,
                        schema=coreschema.String(11),
                        description="User's CPF"
                    ),
                    coreapi.Field(
                        name='phone_number',
                        location='form',
                        required=False,
                        schema=coreschema.String(30),
                        description="User's phone number"
                    ),
                    coreapi.Field(
                        name='twitter_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(15),
                        description="User's Twitter account username"
                    ),
                    coreapi.Field(
                        name='facebook_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(50),
                        description="User's Facebook account username"
                    ),
                    coreapi.Field(
                        name='linkedin_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(60),
                        description="User's LinkedIn account username"
                    ),
                    coreapi.Field(
                        name='instagram_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(30),
                        description="User's Instagram account username"
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
                        name='nationality',
                        location='form',
                        required=True,
                        schema=coreschema.String(80),
                        description="This is the user's nationality."
                    ),
                    coreapi.Field(
                        name='cpf',
                        location='form',
                        required=False,
                        schema=coreschema.String(11),
                        description="User's CPF"
                    ),
                    coreapi.Field(
                        name='phone_number',
                        location='form',
                        required=False,
                        schema=coreschema.String(30),
                        description="User's phone number"
                    ),
                    coreapi.Field(
                        name='twitter_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(15),
                        description="User's Twitter account username"
                    ),
                    coreapi.Field(
                        name='facebook_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(50),
                        description="User's Facebook account username"
                    ),
                    coreapi.Field(
                        name='linkedin_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(60),
                        description="User's LinkedIn account username"
                    ),
                    coreapi.Field(
                        name='instagram_username',
                        location='form',
                        required=False,
                        schema=coreschema.String(30),
                        description="User's Instagram account username"
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

        # Optionals
        languages: str = request.data.get('languages', None)
        gender: str = request.data.get('gender', 'NI')
        birth_date: str = request.data.get('birth_date', None)
        age: int = request.data.get('age', None)
        biography: str = request.data.get('biography', None)
        company: str = request.data.get('company', None)
        locale: str = request.data.get('locale', None)
        website: str = request.data.get('website', None)
        image = request.FILES.get('image', None)
        email_confirmed: bool = request.data.get('email_confirmed', False)
        recovery_key: str = request.data.get('recovery_key', None)
        cover_color: str = request.data.get('cover_color', DEFAULT_COVER_COLOR)
        primary_color: str = request.data.get('primary_color', DEFAULT_PRIMARY_COLOR)
        secondary_color: str = request.data.get('secondary_color', DEFAULT_SECONDARY_COLOR)
        banned: bool = request.data.get('banned', False)
        must_reset_password: bool = request.data.get('reset_password', False)
        nationality: str = request.data.get('nationality', None)
        cpf: str = request.data.get('cpf', None)
        phone_number: str = request.data.get('phone_number', None)
        twitter_username: str = request.data.get('twitter_username', None)
        facebook_username: str = request.data.get('facebook_username', None)
        linkedin_username: str = request.data.get('linkedin_username', None)
        instagram_username: str = request.data.get('instagram_username', None)
        formatted_birth_date: date | None = None

        # Username validations
        if not username and not bypass_required:
            return generate_error_response('User username is required')

        if username and not isinstance(username, str):
            return generate_error_response('User username must be a string')

        user: user_model | None = User.objects.all().filter(username=username).first()

        if username and user is None:
            return generate_error_response('This username does not exist')

        # Languages validations
        if languages is not None and not isinstance(languages, list):
            return generate_error_response('Languages must be an array of strings')

        # Gender validations
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
            if 'true' == str(banned).lower():
                banned = True
            elif 'false' == str(banned).lower():
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

        # Nationality validations
        if not nationality and not bypass_required:
            return generate_error_response('Nationality is required')

        if nationality and not isinstance(nationality, str):
            return generate_error_response("Nationality must be a string")

        if nationality and len(nationality) > 80:
            return generate_error_response("Nationality must have a max length of 80 characters")

        # CPF validations
        if cpf and not isinstance(cpf, str):
            return generate_error_response("CPF must be a string")

        if cpf and len(cpf) > 11:
            return generate_error_response("CPF must have a max length of 11 characters")

        if cpf:
            try:
                int(cpf)
            except ValueError:
                return generate_error_response("CPF must be only numbers")

        # Phone number validations
        if phone_number and not isinstance(phone_number, str):
            return generate_error_response("Phone number must be a string")

        if phone_number and len(phone_number) > 30:
            return generate_error_response("Phone number must have a max length of 30 characters")

        # Twitter username validations
        if twitter_username and not isinstance(twitter_username, str):
            return generate_error_response("Twitter username must be a string")

        if twitter_username and len(twitter_username) > 15:
            return generate_error_response("Twitter username must have a max length of\
                                            15 characters")

        # Facebook username validations
        if facebook_username and not isinstance(facebook_username, str):
            return generate_error_response("Facebook username must be a string")

        if facebook_username and len(facebook_username) > 50:
            return generate_error_response("Facebook username must have a max length of\
                                            50 characters")

        # LinkedIn username validations
        if linkedin_username and not isinstance(linkedin_username, str):
            return generate_error_response("LinkedIn username must be a string")

        if linkedin_username and len(linkedin_username) > 60:
            return generate_error_response("LinkedIn username must have a max length of\
                                            60 characters")

        # Instagram username validations
        if instagram_username and not isinstance(instagram_username, str):
            return generate_error_response("Instagram username must be a string")

        if instagram_username and len(instagram_username) > 30:
            return generate_error_response("Instagram username must have a max \
                                           length of 30 characters")

        # Data conversion and handling
        data: dict[str, user_model | str | int | list[int] | list[str] | bool | date | None] = {
            'user': user,
            'languages': languages,
            'gender': gender,
            'birth_date': formatted_birth_date,
            'age': int(age) if isinstance(age, str) else None,
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
            'nationality': nationality,
            'cpf': cpf,
            'phone_number': phone_number,
            'twitter_username': twitter_username,
            'facebook_username': facebook_username,
            'linkedin_username': linkedin_username,
            'instagram_username': instagram_username
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
            data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                     "User Profile found")
            serializer = serializers.UserProfileSerializer(user_profile)
            serializer_data = serializer.data
            try:
                # type: ignore
                serializer_data['image'] = f"/media{user_profile.image.path.split('/media')[1]}"
            except IndexError:
                serializer_data['image'] = None

            data['content'] = serializer_data
            return Response(data=data, status=data.get('status', status.HTTP_200_OK))

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

        email_confirmed = profile_data.get('email_confirmed', False)  # type: ignore
        email_confirmed = email_confirmed if email_confirmed is not None else False
        cover_color = profile_data.get('cover_color', DEFAULT_COVER_COLOR)
        cover_color = cover_color if cover_color is not None else DEFAULT_COVER_COLOR
        primary_color = profile_data.get('primary_color', DEFAULT_PRIMARY_COLOR)
        primary_color = primary_color if primary_color is not None else DEFAULT_PRIMARY_COLOR
        secondary_color = profile_data.get('secondary_color', DEFAULT_SECONDARY_COLOR)
        secondary_color = secondary_color if secondary_color is not None else DEFAULT_SECONDARY_COLOR
        banned = False
        must_reset_password = profile_data.get('must_reset_password', False)  # type: ignore
        must_reset_password = must_reset_password if must_reset_password is not None else False

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
                                     email_confirmed=email_confirmed,
                                     recovery_key=profile_data.get(
                                         'recovery_key', ''),
                                     gender=profile_data.get('gender', 'NI'),
                                     cover_color=cover_color,
                                     primary_color=primary_color,
                                     secondary_color=secondary_color,
                                     banned=banned,
                                     must_reset_password=must_reset_password,
                                     nationality=profile_data.get('nationality', ''),
                                     cpf=profile_data.get('cpf', ''),
                                     phone_number=profile_data.get('phone_number', ''),
                                     twitter_username=profile_data.get('twitter_username', ''),
                                     facebook_username=profile_data.get('facebook_username', ''),
                                     linkedin_username=profile_data.get('linkedin_username', ''),
                                     instagram_username=profile_data.get('instagram_username', '')
                                     )

        if profile_data.get('image', None):  # TODO: Image posting is not working
            profile.image = profile_data.get('image')  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "User profile created successfully")
        data = serializers.CreateUserProfileSerializer(profile, many=False).data
        if not profile_data.get('image', None):
            try:
                del data['languages']
                del data['image']
            except Exception:
                pass
        serializer = serializers.CreateUserProfileSerializer(data=data)
        if serializer.is_valid():
            profile.save()

            languages = profile_data.get('languages', None)
            if languages is not None:
                profile = models.UserProfile.objects.get(user__pk=serializer.data['user'])
                for language in languages:  # type: ignore
                    obj, __ = models.UserProfileLanguages.objects.get_or_create(language=language)
                    profile.languages.add(obj)
                profile.save()

            data = serializers.UserProfileSerializer(profile, many=False).data
            try:
                data['image'] = f"/media{profile.image.path.split('/media')[1]}"  # type: ignore
            except IndexError:
                data['image'] = None
            response_data['content'] = data
            return Response(response_data,
                            status=response_data.get('status', status.HTTP_201_CREATED))
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

        if profile_data.get('languages', None):
            languages: list[str] = profile_data.get('languages', None)  # type: ignore
            if languages is not None:
                for language in languages:  # type: ignore
                    obj, __ = models.UserProfileLanguages.objects.get_or_create(language=language)
                    user_profile.languages.add(obj)
                user_profile.save()

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

        if profile_data.get('nationality', None):
            nationality: str = profile_data.get('nationality', None)  # type: ignore
            user_profile.nationality = nationality

        if profile_data.get('cpf', None):
            cpf: str = profile_data.get('cpf', None)  # type: ignore
            user_profile.cpf = cpf

        if profile_data.get('phone_number', None):
            phone_number: str = profile_data.get('phone_number', None)  # type: ignore
            user_profile.phone_number = phone_number

        if profile_data.get('twitter_username', None):
            twitter_username: str = profile_data.get('twitter_username', None)  # type: ignore
            user_profile.twitter_username = twitter_username

        if profile_data.get('facebook_username', None):
            facebook_username: str = profile_data.get('facebook_username', None)  # type: ignore
            user_profile.facebook_username = facebook_username

        if profile_data.get('linkedin_username', None):
            linkedin_username: str = profile_data.get('linkedin_username', None)  # type: ignore
            user_profile.linkedin_username = linkedin_username

        if profile_data.get('instagram_username', None):
            instagram_username: str = profile_data.get('instagram_username', None)  # type: ignore
            user_profile.instagram_username = instagram_username

        try:
            user_profile.clean_fields()
            user_profile.clean()
        except ValidationError as err:
            data = self.generate_basic_response_data(
                status.HTTP_400_BAD_REQUEST, 'Patch data validation error')
            data['errors'] = err
            return Response(data=data, status=data.get('status'))

        user_profile.save()

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "User Profile patched successfully")
        serializer = serializers.UserProfileSerializer(user_profile)
        data = serializer.data
        try:
            data['image'] = f"/media{user_profile.image.path.split('/media')[1]}"  # type: ignore
        except IndexError:
            data['image'] = None
        response_data['content'] = data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
            profile.banned = True
            profile.save()
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
                banned_user.profile.banned = False
                banned_user.profile.save()
                banned_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)

        if slug:
            banned_user = models.BannedUsers.objects.all().filter(profile__slug=slug).first()
            if banned_user is not None:
                banned_user.profile.banned = False
                banned_user.profile.save()
                banned_user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.slug_not_banned_str)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_slug_nor_id_str)


# =================== User Management =================== #
class UserManagementSchema(AutoSchema):
    """Schema for user account"""

    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'User account found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User account not found'
                    }
                }
                return description_generator(title="Get a specific user account.",
                                             description=authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'User account successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create an user account",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'User account successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User account not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from user account",
                                             # noqa: E502
                                             description=authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'User account successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User account not found'
                    }
                }
                return description_generator(title="Delete a specific user account",
                                             description=authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case 'GET':
                return [
                    coreapi.Field(
                        name="username",
                        location="query",
                        required=True,
                        schema=coreschema.String(),
                        description="User account's username"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="username",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="User's account username"
                    ),
                    coreapi.Field(
                        name="password",
                        location='form',
                        required=True,
                        schema=coreschema.String(2),
                        description="User's password"
                    ),
                    coreapi.Field(
                        name="email",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Email address"
                    ),
                    coreapi.Field(
                        name="name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="User's Name"
                    ),
                    coreapi.Field(
                        name="surname",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="User's last name"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="username",
                        location="query",
                        required=True,
                        schema=coreschema.String(),
                        description="User account's username"
                    ),
                    coreapi.Field(
                        name="username",
                        location="form",
                        required=False,
                        schema=coreschema.String(),
                        description="User's account new username"
                    ),
                    coreapi.Field(
                        name="password",
                        location='form',
                        required=False,
                        schema=coreschema.String(2),
                        description="User's password"
                    ),
                    coreapi.Field(
                        name="email",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Email address"
                    ),
                    coreapi.Field(
                        name="name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="User's Name"
                    ),
                    coreapi.Field(
                        name="surname",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="User's last name"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="username",
                        location="query",
                        required=True,
                        schema=coreschema.String(),
                        description="User account's username"
                    )
                ]
            case _:
                return []


class UserManagement(Base):
    """Manage user profile"""

    not_found_str = "User account not found"

    schema = UserManagementSchema()

    def handle_user_data(self, request,
                            # noqa
                            bypass_required: bool = False) -> tuple[bool, dict[str, str | None] | \
                                                                    Response]:
        """Handle profile data"""
        def generate_error_response(text: str) -> tuple[bool, Response]:
            return (False, self.generate_basic_response(status.HTTP_400_BAD_REQUEST, text))

        current_username = request.query_params.get('username', None)

        # Required
        username: str = request.data.get('username', None)
        password: str = request.data.get('password', None)

        # Optional
        email: str = request.data.get('email', None)
        name: str = request.data.get('name', None)
        surname: str = request.data.get('surname', None)

        # Username validations
        if not username and not bypass_required:
            return generate_error_response('User username is required')

        if username and not isinstance(username, str):
            return generate_error_response('User username must be a string')

        user: user_model | None = User.objects.all().filter(username=username).first()

        if username and current_username is not None:
            if user is not None and username != current_username:
                return generate_error_response('This username already exist')
        else:
            if username and user is not None:
                return generate_error_response('This username already exist')

        # Password validations
        if not password and not bypass_required:
            return generate_error_response('Password is required')

        if password and not isinstance(password, str):
            return generate_error_response('Password must be a string')

        # Email validations
        if email and not isinstance(email, str):
            return generate_error_response('Email must be a string')

        # Name validations
        if name and not isinstance(name, str):
            return generate_error_response('Name must be a string')

        # Surname validations
        if surname and not isinstance(surname, str):
            return generate_error_response('Surname must be a string')

        # Data conversion and handling
        data: dict[str, str | None] = {
            'username': username,
            'password': password,
            'email': email,
            'name': name,
            'surname': surname
        }

        return (True, data)

    def get(self, request):
        """Get request"""
        username = request.query_params.get('username', None)

        if username is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_str)

        user_account = User.objects.all().filter(username=username).first()

        if user_account is not None:
            data = self.generate_basic_response_data(status.HTTP_200_OK, "User account found")
            serializer = serializers.UserSerializer(user_account)
            data['content'] = serializer.data
            return Response(data=data, status=data.get('status', status.HTTP_200_OK))

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_str)

    def post(self, request):
        """Post request"""
        data_valid, data_or_response = self.handle_user_data(request)
        if not data_valid:
            return data_or_response

        account_data = data_or_response

        new_username = account_data.get('username', None)

        account = User(username=new_username,
                       email=account_data.get('email', ''),
                       first_name=account_data.get('name', ''),
                       last_name=account_data.get('surname', ''))

        account.set_password(account_data.get('password', None))

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "User account created successfully")
        data = serializers.UserSerializer(account, many=False).data
        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data['content'] = serializer.data
            return Response(response_data,
                            status=response_data.get('status', status.HTTP_201_CREATED))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Patch request"""
        username = request.query_params.get('username', None)

        if username is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_str)

        user_account = User.objects.all().filter(username=username).first()

        if user_account is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_str)

        data_valid, data_or_response = self.handle_user_data(
            request, bypass_required=True)
        if not data_valid:
            return data_or_response

        account_data = data_or_response

        if account_data.get('username', None):
            new_username: str = account_data.get('username', None)  # type: ignore
            user_account.username = new_username  # type: ignore

        if account_data.get('password', None):
            password: str = account_data.get('password', None)  # type: ignore
            if authenticate(request, username=username, password=password) is None:
                user_account.set_password(password)

        if account_data.get('email', None):
            email: str = account_data.get('email', '')  # type: ignore
            user_account.email = email  # type: ignore

        if account_data.get('name', None):
            name: str = account_data.get('name', 0)  # type: ignore
            user_account.first_name = name  # type: ignore

        if account_data.get('surname', None):
            surname: str = account_data.get('surname', date.today())  # type: ignore
            user_account.last_name = surname  # type: ignore

        try:
            user_account.clean()  # type: ignore
        except ValidationError as err:
            data = self.generate_basic_response_data(status.HTTP_400_BAD_REQUEST,
                                                     'Patch data validation error')
            data['errors'] = err
            return Response(data=data, status=data.get('status'))

        user_account.save()  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "User Profile patched successfully")
        serializer = serializers.UserSerializer(user_account)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def delete(self, request):
        """Delete request"""
        username = request.query_params.get('username', None)

        if username is not None:
            user_account = User.objects.all().filter(username=username).first()

            if user_account is not None:
                user_account.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_str)
