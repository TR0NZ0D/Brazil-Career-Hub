from .permissions import AuthenticateApiClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tools import api_tools as tools
from api_admins.models import ApiAdmin
from django.contrib.auth.models import User
from django.contrib import auth
from typing import TypeAlias, Optional, Any
from uuid import uuid4
from hashlib import md5, sha512


class Base(APIView):
    permission_classes = [AuthenticateApiClient]
    __api_token__: TypeAlias = Optional[str]
    __response_data__: TypeAlias = dict[str, Any]
    authenticated_user: Optional[User] = None

    def generate_api_token(self) -> str:
        uuid = str(uuid4())
        token_md5 = md5(uuid.encode())
        token_sha512 = sha512(uuid.encode())
        token_md5_sha512 = sha512(str(token_md5).encode())
        token = sha512(f'{token_sha512}{token_md5_sha512}'.encode()).hexdigest()
        token = (token[:250]) if len(token) > 255 else token
        return token

    def get_token(self, request, username: Optional[str] = None, password: Optional[str] = None, user: Optional[User] = None) -> __api_token__:
        if (username is None) and (password is None) and (user is None):
            return request.headers.get('token', None)

        if user is not None:
            authenticated_user = user

            if not user.is_staff:
                return None
        else:
            auth_user = auth.authenticate(request, username=username, password=password)

            if auth_user is None:
                return None

            authenticated_user = User.objects.all().filter(username=auth_user.get_username()).first()  # type: ignore [assignment]

            if (authenticated_user is None) or (not authenticated_user.is_staff):
                return None

        self.authenticated_user = authenticated_user
        api_admin = ApiAdmin.objects.all().filter(user=authenticated_user).first()

        if api_admin is None:
            return None

        return api_admin.token

    def generate_basic_response(self, status: int, message: str) -> Response:
        data = self.generate_basic_response_data(status, message)
        return Response(data=data, status=data.get('status'))

    def generate_basic_response_data(self, status: int, message: str) -> __response_data__:
        return {
            'status': status,
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
            'response': self.generate_basic_response(status.HTTP_304_NOT_MODIFIED, 'Token request returned with default values')
        }

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
                response_dict['response'] = self.generate_basic_response(status.HTTP_401_UNAUTHORIZED, error_string)
                return response_dict

            token = self.get_token(request, username, password)
        else:
            user = User.objects.all().filter(username=request.user.get_username()).first()
            token = self.get_token(request, user=user)

            if user is None:
                response_dict['found'] = False
                response_dict['token'] = None
                response_dict['response'] = self.generate_basic_response(status.HTTP_401_UNAUTHORIZED, 'Missing credentials dict in headers')
                return response_dict

            self.authenticated_user = user

        if token is None:
            response_dict['found'] = False
            response_dict['token'] = None
            response_dict['response'] = self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'API token not found')
            return response_dict

        response_dict['found'] = True
        response_dict['token'] = token
        response_dict['response'] = None
        return response_dict


class ApiTesting(Base):  # TODO: Remove before sending to prod
    """Endpoint for testing API requests and responses"""
    def get(self, request, format=None):
        """
Get basic info from back-end (used only for debugging, useless in front-end)
---
    Authorization:
        Type: API Key
        Key: 'token'
        Add to: header

    Response body:
    {
        'user': username (str),
        'data': request data (json),
        'auth': authentication (str),
        'query_params': query parameters (json),
        'accepted_media_type': accepted media type (str),
        'method': request method (str),
        'content_type': content type (str),
        'scheme': scheme (str),
        'body': body (str),
        'path': request path (str),
        'path_info': same as request path (str),
        'encoding': request encoding,
        'content_params': content parameters (json),
        'COOKIES': request cookies (json),
        'headers': request headers (json),
        'token': api token for request (str)
    }
    """
        data = {
            'user': f'{request.user}',
            'data': request.data,
            'auth': f'{request.auth}',
            'query_params': request.query_params,
            'accepted_media_type': request.accepted_media_type,
            'method': request.method,
            'content_type': request.content_type,
            'scheme': request.scheme,
            'body': request.body,
            'path': request.path,
            'path_info': request.path_info,
            'encoding': request.encoding,
            'content_params': request.content_params,
            'COOKIES': request.COOKIES,
            'headers': request.headers,
            'token': self.get_token(request)
        }
        return Response(data=data, status=status.HTTP_200_OK)


# =================== API Built-In Info ===================
class ApiStatus(Base):
    """Endpoint to check API reachability."""

    def get(self, request, format=None):
        """
Check API reachability.
---
    Authorization:
        Type: API Key
        Key: 'token'
        Add to: header

    Response body:
        {
            'status': response status code (int),
            'message': response message (str)
        }
    """
        return self.generate_basic_response(status.HTTP_200_OK, 'API running')


class ApiVersion(Base):
    """API version and its environment"""

    def get(self, request, format=None):
        """
Returns API's current version and environment
---
    Authorization:
        Type: API Key
        Key: 'token'
        Add to: header

    Response body:
        {
            'status': response status code (int),
            'message': response message (str),
            'version': API's current version and environment (str)
        }
    """
        data = self.generate_basic_response_data(status.HTTP_200_OK, 'API version')
        data['version'] = tools.generate_version()
        return Response(data=data, status=data.get('status'))


# =================== API Security & Credentials ===================
class AuthToken(Base):
    """Manage API access token"""
    def get(self, request):
        """
Get user API authentication token
---
    Authorization:
        None

    Required parameter in header:
        'username': username (str)
        'password': password (str)

    Response body:
        {
            'status': response status code (int),
            'message': response message (str),
            'token': user's API token (str)
        }
    """
        validation = self.get_token_or_response(request)
        fallback_response = self.generate_basic_response(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Fallback response from token validation')

        if not validation.get('found', False):
            return validation.get('response', fallback_response)
        else:
            data = self.generate_basic_response_data(status.HTTP_200_OK, f'API token for user: {self.authenticated_user.get_username() if self.authenticated_user is not None else "Unknown"}')
            data['token'] = validation.get('token')
            return Response(data=data, status=data.get('status'))

    def post(self, request):
        """
Create API token.
---
    Authorization:
        None

    Requirements:
        - User must exist in back-end users database
        - User must have admin permissions and access to back-end admin page

    Required parameter in header:
        'username': username (str)
        'password': password (str)

    Response body:
        {
            'status': response status code (int),
            'message': response message (str),
            'token': user's created API token (str)
        }
        """
        username = request.headers.get('username', None)
        password = request.headers.get('password', None)
        if (username is not None) and (password is not None):
            if username is None or password is None:
                return self.generate_basic_response(status.HTTP_401_UNAUTHORIZED, 'Missing credentials dict in headers')

            authenticated_user = auth.authenticate(request, username=username, password=password)

            if authenticated_user is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'User not found')

            user = User.objects.all().filter(username=authenticated_user.get_username()).first()
        else:
            user = User.objects.all().filter(username=request.user.get_username()).first()

        if user is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, 'User not found')

        if not user.is_staff:
            return self.generate_basic_response(status.HTTP_403_FORBIDDEN, 'User does not have permission to perform this action')

        self.authenticated_user = user

        api_admin, _ = ApiAdmin.objects.get_or_create(user=user)

        if not api_admin.token:
            api_admin.token = self.generate_api_token()
            api_admin.save()

        token = api_admin.token

        data = self.generate_basic_response_data(status.HTTP_200_OK, f'API Token created for: {self.authenticated_user.get_username()}')
        data['token'] = token
        return Response(data=data, status=status.HTTP_202_ACCEPTED)
