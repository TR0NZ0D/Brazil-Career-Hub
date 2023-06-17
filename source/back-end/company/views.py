"""
company/views.py

Created by: Gabriel Menezes de Antonio
"""
import coreapi  # type: ignore
import coreschema  # type: ignore

from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from api.tools.api_tools import description_generator
from api.views import Base

from . import models
from . import serializers


# =================== API Security & Credentials =================== #
class CompanyAccountSchema(AutoSchema):
    """Schema for company account"""

    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

Inform PK or slug if mentioning specific company account, PK will prevail if both fields are sent

"""
        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Company account found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Company account not found'
                    }
                }
                return description_generator(title="Get a specific Company account.",
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
                        description="Company Account ID"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(min_length=2),
                        description="Company Account slug"
                    )
                ]
            case _:
                return []


class CompanyAccount(Base):
    """Manages API's authentication token"""

    schema = CompanyAccountSchema()

    not_found_id_str = "Company account ID not found"
    not_found_slug_str = "Company account slug not found"
    not_found_account_str = "Company account not found"

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

            company_account = models.CompanyAccountModel.objects.all().filter(slug=slug).first()
        else:
            if not primary_key:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_id_str)

            company_account = models.CompanyAccountModel.objects.all() \
                .filter(pk=primary_key).first()

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "")
        if company_account is not None:
            serializer = serializers.CompanyAccountSerializer(company_account)
            response_data['content'] = join_tables(serializer.data)
            return Response(data=response_data, status=status.HTTP_200_OK)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)


def join_tables(account_data: dict | None = None) -> dict:
    """Concatenates company profile data into company account data

    Args:
        account_data (dict, optional): Company account data. Defaults to None.

    Returns:
        dict: Joined company account data + company profile data
    """
    # TODO: Include profile data
    profile_data: dict = {}
    if account_data is not None:
        joined_data = account_data
        joined_data.update(profile_data)
        return joined_data

    return profile_data
