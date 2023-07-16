"""
company/views.py

Created by: Gabriel Menezes de Antonio
"""
import coreapi  # type: ignore
import coreschema  # type: ignore

from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from api.tools.constants import (registration_status__str__, legal_nature__str__)
from api.tools.api_tools import description_generator
from api.views import Base

from . import models
from . import serializers


# =================== Company Account =================== #
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

        choices_info = f"""

## Available Registration Statuses

{registration_status__str__}

## Available Legal Natures

{legal_nature__str__}
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
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Company account successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create an Company account",
                                             description=authorization_info + choices_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Company account successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Company account ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from company account",
                                             # noqa: E502
                                             description=query_params_info + authorization_info + choices_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Company account successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Company account not found'
                    }
                }
                return description_generator(title="Delete a specific company account",
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
            case 'POST':
                return [
                    coreapi.Field(
                        name="cpnj",
                        location="form",
                        required=True,
                        schema=coreschema.String(15),
                        description="Company cnpj"
                    ),
                    coreapi.Field(
                        name="corporate_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(100),
                        description="Company's corporate name"
                    ),
                    coreapi.Field(
                        name="registration_status",
                        location='form',
                        required=False,
                        schema=coreschema.String(1),
                        description="Company's registration status"
                    ),
                    coreapi.Field(
                        name="fantasy_name",
                        location='form',
                        required=True,
                        schema=coreschema.String(60),
                        description="Company's fantasy name"
                    ),
                    coreapi.Field(
                        name="cnae",
                        location='form',
                        required=True,
                        schema=coreschema.Integer(),
                        description="Company's cnae"
                    ),
                    coreapi.Field(
                        name="legal_nature",
                        location='form',
                        required=False,
                        schema=coreschema.String(6),
                        description="Company's legal nature"
                    )
                ]
            case 'PATCH':
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
                    ),
                    coreapi.Field(
                        name="cpnj",
                        location="form",
                        required=False,
                        schema=coreschema.String(15),
                        description="Company cnpj"
                    ),
                    coreapi.Field(
                        name="corporate_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(100),
                        description="Company's corporate name"
                    ),
                    coreapi.Field(
                        name="registration_status",
                        location='form',
                        required=False,
                        schema=coreschema.String(1),
                        description="Company's registration status"
                    ),
                    coreapi.Field(
                        name="fantasy_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(60),
                        description="Company's fantasy name"
                    ),
                    coreapi.Field(
                        name="cnae",
                        location='form',
                        required=False,
                        schema=coreschema.Integer(),
                        description="Company's cnae"
                    ),
                    coreapi.Field(
                        name="legal_nature",
                        location='form',
                        required=False,
                        schema=coreschema.String(6),
                        description="Company's legal nature"
                    )
                ]
            case 'DELETE':
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
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)
    
    def post(self, request): 
        pass
    
    def patch(self, request): 
        pass
    
    def delete(self, request): 
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
        if company_account is not None:
            company_account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)


# =================== Company Profile =================== #
class CompanyProfileSchema(AutoSchema):
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
                        'reason': 'Company profile found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Company profile not found'
                    }
                }
                return description_generator(title="Get a specific Company profile.",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Company profile successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Company account not found'
                    }
                }
                return description_generator(title="Create an Company profile",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Company profile successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Company profile ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from company profile",
                                             # noqa: E502
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Company profile successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Company profile not found'
                    }
                }
                return description_generator(title="Delete a specific company profile",
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
                        description="Company profile ID"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="company_id",
                        location="form",
                        required=True,
                        schema=coreschema.String(15),
                        description="Company account ID"
                    ),
                    coreapi.Field(
                        name="address",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(255)),
                        description="Company's address list (Array should contain two strings and an integer)"
                    ),
                    coreapi.Field(
                        name="contact",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Company's contact information"
                    ),
                    coreapi.Field(
                        name="creation_date",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Company's creation date"
                    ),
                    coreapi.Field(
                        name="financial_capital",
                        location='form',
                        required=False,
                        schema=coreschema.Number(),
                        description="Company's financial capital"
                    ),
                    coreapi.Field(
                        name="employees",
                        location='form',
                        required=False,
                        schema=coreschema.Integer(),
                        description="Company's employees number"
                    ),
                    coreapi.Field(
                        name="site_url",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Company's website URL"
                    ),
                    coreapi.Field(
                        name="social_media",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(255)),
                        description="Company's social media list (Array should contain three Strings)"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Company profile ID"
                    ),
                    coreapi.Field(
                        name="company_id",
                        location="form",
                        required=True,
                        schema=coreschema.String(15),
                        description="Company account ID"
                    ),
                    coreapi.Field(
                        name="address",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(255)),
                        description="Company's address list (Array should contain two strings and an integer)"
                    ),
                    coreapi.Field(
                        name="contact",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Company's contact information"
                    ),
                    coreapi.Field(
                        name="creation_date",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Company's creation date"
                    ),
                    coreapi.Field(
                        name="financial_capital",
                        location='form',
                        required=False,
                        schema=coreschema.Number(),
                        description="Company's financial capital"
                    ),
                    coreapi.Field(
                        name="employees",
                        location='form',
                        required=False,
                        schema=coreschema.Integer(),
                        description="Company's employees number"
                    ),
                    coreapi.Field(
                        name="site_url",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Company's website URL"
                    ),
                    coreapi.Field(
                        name="social_media",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(255)),
                        description="Company's social media list (Array should contain three Strings)"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Company profile ID"
                    )
                ]
            case _:
                return []

class CompanyProfile(Base):
    schema = CompanyProfileSchema()

    not_found_id_str = "Company profile ID not found"
    not_found_account_str = "Company profile not found"

    def get(self, request, *args, **kwargs):
        pk = request.query_params.get("pk", None)
        if not pk:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)
        company_profile = models.CompanyProfileModel.objects.filter(pk=pk).first()
        if company_profile is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)
        serializer = serializers.CompanyProfileSerializer(company_profile)
        response_data = self.generate_basic_response_data(status.HTTP_200_OK, "")
        response_data["content"] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    def post(self, request): 
        pass
    
    def patch(self, request): 
        pass
    
    def delete(self, request): 
        pk = request.query_params.get("pk", None)
        if not pk:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)
        company_profile = models.CompanyProfileModel.objects.filter(pk=pk).first()
        if company_profile is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)
        company_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
