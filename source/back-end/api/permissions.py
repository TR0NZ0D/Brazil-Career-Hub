from rest_framework import permissions
from django.contrib.auth.models import User
from api_admins.models import ApiAdmin
from django.contrib import auth


class AuthenticateApiClient(permissions.BasePermission):
    """Allow access if user is authenticated and is super user or staff
    or allow access by authenticating its credentials and api token passed in headers
    """

    def has_permission(self, request, view) -> bool:
        # If user is authenticated means that he is in UI docs, allow
        if bool(request.user and request.user.is_authenticated and (request.user.is_superuser) or (request.user.is_staff)):  # type: ignore
            return True

        username = request.headers.get('username', None)
        password = request.headers.get('password', None)
        api_token = request.headers.get('token', None)

        # If none of the required parameters received, deny
        if (username is None) and (password is None) and (api_token is None):
            return False

        # If only username or only password and not api_token, deny
        if (((username is None) and (password)) or ((username) and (password is None))) and (api_token is None):
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

        api_admin = ApiAdmin.objects.all().filter(user=user).first()

        # If Api Admin registry not found, deny
        if api_admin is None:
            return False

        # If token not found, deny
        if not api_admin.token:
            return False

        return True
