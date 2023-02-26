"""
api_admins/views.py

Created by: Gabriel Menezes de Antonio
"""
import coreapi  # type: ignore
import coreschema  # type: ignore
from api.tools.api_tools import description_generator
from api.views import Base
from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from . import models

User = get_user_model()


# =================== API Security & Credentials =================== #
class AuthTokenSchema(AutoSchema):
    """Schema for auth token"""

    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Key:** "username"
**Key:** "password"
**Add to:** header
"""

        no_authorization_info = """
## Authorization:

**None**
"""

        requirements = """
## Requirements:

- User must exist in back-end users database
- User must have admin permissions and access to back-end admin page

"""
        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Successfully fetched API token for authenticated user'
                    },
                    "304": {
                        'description': 'NOT MODIFIED',
                        'reason': 'Token request returned with default values'
                    },
                    "500": {
                        'description': 'INTERNAL SERVER ERROR',
                        'reason': 'Error response not found, fallback'
                    },
                    "401": {
                        'description': 'UNAUTHORIZED',
                        'reason': 'Credentials authentication error'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'API token not found'
                    }
                }
                return description_generator(title="Get user API authentication token",
                                             description=authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Successfully created API token'
                    },
                    "401": {
                        'description': "UNAUTHORIZED",
                        'reason': 'Credentials authentication error'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'User not found'
                    },
                    "403": {
                        'description': "FORBIDDEN",
                        'reason': 'User does not have permission to perform this action'
                    }
                }
                return description_generator(title="Create API access token",
                                             description=requirements + no_authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case 'GET':
                return [
                    coreapi.Field(
                        name="username",
                        location="header",
                        required=True,
                        schema=coreschema.String(1),
                        description="Admin username"
                    ),
                    coreapi.Field(
                        name="password",
                        location="header",
                        required=True,
                        schema=coreschema.String(1),
                        description="Admin password"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="username",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="Admin username"
                    ), coreapi.Field(
                        name="password",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Admin password"
                    )
                ]
            case _:
                return []


class BaseAuthToken(Base):
    """Manages API's authentication token"""

    schema = AuthTokenSchema()

    def get(self, request):
        """Get request"""
        validation = self.get_token_or_response(request)
        fallback_response = self.generate_basic_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            'Fallback response from token validation'
        )

        if not validation.get('found', False):
            return validation.get('response', fallback_response)

        data = self.generate_basic_response_data(
            status.HTTP_200_OK,
            f'API token for user: {self.authenticated_user.get_username() if self.authenticated_user is not None else "Unknown"}')  # type: ignore # pylint: disable=C0301
        data['token'] = validation.get('token')
        return Response(data=data, status=data.get('status'))

    def post(self, request):
        """Post request"""
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if (username is not None) and (password is not None):
            if username is None or password is None:
                return self.generate_basic_response(status.HTTP_401_UNAUTHORIZED,
                                                    'Missing credentials')

            authenticated_user = auth.authenticate(
                request, username=username, password=password)

            if authenticated_user is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'User not found')

            user = User.objects.all().filter(username=authenticated_user.get_username()).first()
        else:
            user = User.objects.all().filter(username=request.user.get_username()).first()

        if user is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'User not found')

        if not user.is_staff:  # type: ignore
            return self.generate_basic_response(
                status.HTTP_403_FORBIDDEN,
                'User does not have permission to perform this action'
            )

        self.authenticated_user = user

        api_admin, _ = models.ApiAdmin.objects.get_or_create(user=user)

        if not api_admin.token:
            api_admin.token = self.generate_api_token()
            api_admin.save()

        token = api_admin.token

        data = self.generate_basic_response_data(
            status.HTTP_201_CREATED,
            f'API Token created for: {self.authenticated_user.get_username()}'
        )
        data['token'] = token
        return Response(data=data, status=data.get('status'))
