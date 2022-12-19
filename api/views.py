from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tools import api_tools as tools


# =================== API Built-In Info ===================
class ApiStatus(APIView):
    """Return status code 200 if the API was successfully called. Can be used to check if it is reachable."""

    def get(self, request, format=None):
        data = {
            'status': status.HTTP_200_OK,
            'description': 'API running'
        }
        return Response(data=data, status=data.get('status'))


class ApiVersion(APIView):
    """Returns the current API version with the environment."""

    def get(self, request, format=None):
        data = {
            'status': status.HTTP_200_OK,
            'description': 'API version',
            'version': tools.generate_version()
        }
        return Response(data=data, status=data.get('status'))
