"""
api/views.py

Created by: Gabriel Menezes de Antonio
"""
from hashlib import md5, sha512
from typing import Any, Optional, TypeAlias
from uuid import uuid4
from random import randint

import coreapi  # type: ignore

from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema
from rest_framework.views import APIView

from api.tools.api_tools import description_generator
from api_admins.models import ApiAdmin

from .permissions import AuthenticateApiClient
from .tools import api_tools as tools

User = get_user_model()


# =================== Base API Class =================== #
class Base(APIView):
    """Base API class"""
    user_model: TypeAlias = User  # type: ignore
    permission_classes = [AuthenticateApiClient]
    __api_token__: TypeAlias = Optional[str]
    __response_data__: TypeAlias = dict[str, Any]
    authenticated_user: Optional[user_model] = None

    # ======== Error Strings ======== #
    not_found_slug_nor_id_str = "Neither ID nor slug found"

    def generate_api_token(self) -> str:
        """Generate API token"""
        uuid = str(uuid4())
        token_md5 = md5(uuid.encode())
        token_sha512 = sha512(uuid.encode())
        token_md5_sha512 = sha512(str(token_md5).encode())
        token = sha512(f'{token_sha512}{token_md5_sha512}'.encode()).hexdigest()
        token = (token[:250]) if len(token) > 255 else token
        random_start_number = randint(0, len(token) - 34)
        end_number = random_start_number + 32
        final_token = md5(token[random_start_number:end_number].encode()).hexdigest()
        return final_token

    def get_token(self,
                  request,
                  username: Optional[str] = None,
                  password: Optional[str] = None,
                  user: Optional[user_model] = None) -> __api_token__:
        """Get token from request"""
        if (username is None) and (password is None) and (user is None):
            return request.headers.get('token', None)

        if user is not None:
            authenticated_user = user

            if not user.is_staff:  # type: ignore
                return None
        else:
            auth_user = auth.authenticate(request, username=username, password=password)

            if auth_user is None:
                return None

            authenticated_user = User.objects.all() \
                .filter(username=auth_user.get_username()).first()

            if (authenticated_user is None) or (not authenticated_user.is_staff):  # type: ignore
                return None

        self.authenticated_user = authenticated_user
        api_admin = ApiAdmin.objects.all().filter(user=authenticated_user).first()

        if api_admin is None:
            return None

        return api_admin.token

    def generate_basic_response(self, status_code: int, message: str) -> Response:
        """Generates a basic response"""
        data = self.generate_basic_response_data(status_code, message)
        return Response(data=data, status=data.get('status'))

    def generate_basic_response_data(self, status_code: int, message: str) -> __response_data__:
        """Generates a basic response data"""
        return {
            'status': status_code,
            'message': message
        }

    def get_token_or_response(self, request) -> dict[str, bool | Optional[str] | Response]:
        """Returns a dict with a token if found or an error response

        Args:
            request (HttpRequest): Request received from REST

        Returns:
            {
                'found': is token found (bool),
                'token': token (str | None),
                'response': response if not found (Response | None)
            }
        """
        response_dict: dict[str, bool | Optional[str] | Response] = {
            'found': False,
            'token': None,
            'response': self.generate_basic_response(status.HTTP_304_NOT_MODIFIED,
                                                     'Token request returned with default values')
        }

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if (username is None) and (password is None):
            username = request.headers.get('username', None)
            password = request.headers.get('password', None)

        if (username is not None) and (password is not None):

            error_string = ''

            if username is None:
                error_string += 'Missing username'

            if password is None:
                error_string += 'Missing password' if not error_string else ' and password'

            if error_string:
                error_string += ' credential' if 'password' not in error_string else ' credentials'
                response_dict['found'] = False
                response_dict['token'] = None
                response_dict['response'] = \
                    self.generate_basic_response(status.HTTP_401_UNAUTHORIZED, error_string)
                return response_dict

            token = self.get_token(request, username, password)
        else:
            user = User.objects.all().filter(username=request.user.get_username()).first()
            token = self.get_token(request, user=user)

            if user is None:
                response_dict['found'] = False
                response_dict['token'] = None
                response_dict['response'] = \
                    self.generate_basic_response(status.HTTP_401_UNAUTHORIZED,
                                                 'Missing credentials')
                return response_dict

            self.authenticated_user = user

        if token is None:
            response_dict['found'] = False
            response_dict['token'] = None
            response_dict['response'] = \
                self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'API token not found')
            return response_dict

        response_dict['found'] = True
        response_dict['token'] = token
        response_dict['response'] = None
        return response_dict


# =================== API Built-In Info =================== #
class StatusSchema(AutoSchema):
    """Schema for status endpoint"""
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
                        'reason': 'API reachable and responsive'
                    }
                }
                return description_generator(title="Check API reachability",
                                             description=authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case _:
                return []


class ApiStatus(Base):
    """Checks API reachability."""

    schema = StatusSchema()

    def get(self, request):
        """Get request"""
        return self.generate_basic_response(status.HTTP_200_OK, 'API running')


class VersionSchema(AutoSchema):
    """Schema for version endpoint"""
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
                        'reason': 'API Version and environment fetched successfully'
                    },
                }
                return description_generator(title="Fetches API version and environment",
                                             description=authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case _:
                return []


class ApiVersion(Base):
    """Returns API version and its environment"""

    schema = VersionSchema()

    def get(self, request):
        """Get request"""
        data = self.generate_basic_response_data(status.HTTP_200_OK, 'API version')
        data['version'] = tools.generate_version()
        return Response(data=data, status=data.get('status'))
