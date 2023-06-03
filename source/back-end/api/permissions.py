"""
api/permissions.py

Created by: Gabriel Menezes de Antonio
"""
from django.contrib import auth
from django.contrib.auth import get_user_model

from rest_framework import permissions

from api_admins.models import ApiAdmin

User = get_user_model()


class AuthenticateApiClient(permissions.BasePermission):
    """Allow access if user is authenticated and is super user or staff
    or allow access by authenticating its credentials and api token passed in headers
    """

    def has_permission(self, request, view) -> bool:
        # If user is authenticated means that he is in UI docs, allow
        if request.user and request.user.is_authenticated \
           and ((request.user.is_superuser) or (request.user.is_staff)):  # type: ignore
            return True

        username = request.headers.get('username', None)
        password = request.headers.get('password', None)
        api_token = request.headers.get('Authorization', None)

        if api_token is not None:
            # If Bearer is not in token, deny
            if "Bearer" not in api_token:
                return False

            # Remove Bearer content to validate token
            api_token = api_token.replace("Bearer", "").replace(" ", "")

        # If none of the required parameters received, deny
        if (username is None) and (password is None) and (api_token is None):
            return False

        # If only username or only password and not api_token, deny
        if (((username is None) and (password)) or ((username) and (password is None))) \
           and (api_token is None):
            return False

        # If token exists, allow
        if (api_token is not None) and (ApiAdmin.objects.all().filter(token=api_token).exists()):
            return True

        auth_user = auth.authenticate(request, username=username, password=password)

        # If credentials didn't authenticate, deny
        if auth_user is None:
            return False

        user = User.objects.all().filter(username=auth_user.get_username()).first()

        # If user not found, deny
        if user is None:
            return False

        # IF user is not staff, deny
        if not user.is_staff:  # type: ignore
            return False

        api_admin = ApiAdmin.objects.all().filter(user=user).first()

        # This means that the user is trying to get or request a token, allow
        if (api_admin is None) and ("api_admins.views.BaseAuthToken" in str(view)):
            return True

        # If Api Admin registry not found, deny
        if api_admin is None:
            return False

        # If token not found, deny
        if not api_admin.token:
            return False

        return True
