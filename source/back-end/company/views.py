"""
company/views.py

Created by: Gabriel Menezes de Antonio
"""
from datetime import date

import coreapi  # type: ignore
import coreschema  # type: ignore

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema
from tr0nz0d.tools.cnpj import CNPJ

from api.tools.api_tools import description_generator
from api.tools.constants import (legal_nature__str__, legal_nature_keys,
                                 registration_status__str__,
                                 registration_status_keys)
from api.views import Base

from . import models, serializers


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
                        name="cnpj",
                        location="form",
                        required=True,
                        schema=coreschema.String(15),
                        description="Company cnpj"
                    ),
                    coreapi.Field(
                        name="password",
                        location="form",
                        required=True,
                        schema=coreschema.String(),
                        description="Company's password"
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
                        name="cnpj",
                        location="form",
                        required=False,
                        schema=coreschema.String(15),
                        description="Company cnpj"
                    ),
                    coreapi.Field(
                        name="password",
                        location="form",
                        required=False,
                        schema=coreschema.String(),
                        description="Company password"
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

    def handle_account_data(self, request, bypass_required):

        def generate_error_response(text: str):
            return (False, self.generate_basic_response(status.HTTP_400_BAD_REQUEST, text))
        # Required
        cnpj = request.data.get("cnpj", None)
        password = request.data.get("password", None)
        corporate = request.data.get("corporate_name", None)
        fantasy = request.data.get("fantasy_name", None)
        cnae = request.data.get("cnae", None)
        # Optionals
        registration = request.data.get("registration_status", "1")
        legal_nature = request.data.get("legal_nature", "EI")
        if not password and not bypass_required:
            return generate_error_response("Password is required")
        if password and not isinstance(password, str):
            return generate_error_response("Password should be a string")
        if not cnpj and not bypass_required:
            return generate_error_response("CNPJ is required")
        if cnpj and not CNPJ().validar(str(cnpj)):
            return generate_error_response("CNPJ is invalid")
        if cnpj and models.CompanyAccountModel.objects.filter(cnpj=cnpj).exists():
            return generate_error_response("CNPJ is already registered")
        if not corporate and not bypass_required:
            return generate_error_response("Corporate name is required")
        if corporate and len(corporate) > 100:
            return generate_error_response("Corporate name must up to 100 characters")
        if not fantasy and not bypass_required:
            return generate_error_response("Fantasy name is required")
        if fantasy and len(fantasy) > 60:
            return generate_error_response("Fantasy name must up to 60 characters")
        if not cnae and not bypass_required:
            return generate_error_response("CNAE is required")
        if cnae:
            try:
                cnae = int(cnae)
            except ValueError:
                return generate_error_response("CNAE must be an integer")
        if registration and not isinstance(registration, str):
            return generate_error_response("Registration status must be a String")
        if registration and registration not in registration_status_keys:
            return generate_error_response(f"Registration status {registration} is not available")
        if legal_nature and not isinstance(legal_nature, str):
            return generate_error_response("Legal nature must be a String")
        if legal_nature and legal_nature not in legal_nature_keys:
            return generate_error_response(f"Legal nature {legal_nature} is not available")
        data = {
            "cnpj": cnpj,
            "password": password,
            "corporate": corporate,
            "fantasy": fantasy,
            "cnae": cnae,
            "registration": registration,
            "legal_nature": legal_nature
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

            company_account = models.CompanyAccountModel.objects.all().filter(slug=slug).first()
        else:
            if not primary_key:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_id_str)

            company_account = models.CompanyAccountModel.objects.all() \
                .filter(pk=primary_key).first()

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Company's account found")
        if company_account is not None:
            serializer = serializers.CompanyAccountSerializer(company_account)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)

    def post(self, request):
        data_valid, data_or_response = self.handle_account_data(request, False)
        if not data_valid:
            return data_or_response
        account_data = data_or_response
        cnpj = account_data.get("cnpj", None)
        password = account_data.get("password", "")
        corporate = account_data.get("corporate", None)
        fantasy = account_data.get("fantasy", None)
        cnae = account_data.get("cnae", None)
        registration = account_data.get("registration", "1")
        legal_nature = account_data.get("legal_nature", "EI")

        account = models.CompanyAccountModel(
            cnpj=cnpj,
            password=password,
            corporate_name=corporate,
            registration_status=registration,
            fantasy_name=fantasy,
            cnae=cnae,
            legal_nature=legal_nature
        )
        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED, "Company account created successfully")
        data = serializers.CreateCompanyAccountSerializer(account, many=False).data
        serializer = serializers.CreateCompanyAccountSerializer(data=data)
        if serializer.is_valid():
            account.save()
            data = serializers.CompanyAccountSerializer(account, many=False).data
            response_data["content"] = data
            return Response(response_data, status=response_data.get("status", status.HTTP_201_CREATED))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
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
        if company_account is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)
        data_valid, data_or_response = self.handle_account_data(request, True)
        if not data_valid:
            return data_or_response
        account_data = data_or_response

        if account_data.get("cnpj", None):
            cnpj = account_data.get("cnpj", None)
            company_account.cnpj = cnpj
        if account_data.get("password", None):
            password = account_data.get("password", None)
            company_account.password = password
        if account_data.get("corporate", None):
            corporate = account_data.get("corporate", None)
            company_account.corporate_name = corporate
        if account_data.get("fantasy", None):
            fantasy = account_data.get("fantasy", None)
            company_account.fantasy_name = fantasy
        if account_data.get("cnae", None):
            cnae = account_data.get("cnae", None)
            company_account.cnae = cnae
        if account_data.get("registration", None):
            registration = account_data.get("registration", "1")
            company_account.registration_status = registration
        if account_data.get("legal_nature", None):
            legal_nature = account_data.get("legal_nature", "EI")
            company_account.legal_nature = legal_nature
        try:
            company_account.clean_fields()
            company_account.clean()
        except ValidationError as error:
            data = self.generate_basic_response_data(status.HTTP_400_BAD_REQUEST, "Patch data validation error")
            data["errors"] = error
            return Response(data=data, status=data.get("status"))
        company_account.save()
        response_data = self.generate_basic_response_data(status.HTTP_200_OK, "Company account patched successfully")
        serializer = serializers.CompanyAccountSerializer(company_account)
        response_data["content"] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
                        description="Company's address list (JSON should contain two strings and an integer)"
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
                        schema=coreschema.Integer(),
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
                        description="Company's social media list (JSON should contain three Strings)"
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
                        description="Company's address list (JSON should contain two strings and an integer)"
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
                        schema=coreschema.Integer(),
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
                        description="Company's social media list (JSON should contain three Strings)"
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

    def handle_account_data(self, request, bypass_required):

        def generate_error_response(text: str):
            return (False, self.generate_basic_response(status.HTTP_400_BAD_REQUEST, text))
        # Required
        company_pk = request.data.get("company_id", None)
        # Optionals
        address = request.data.get("address", None)
        contact = request.data.get("contact", None)
        creation_date = request.data.get("creation_date", None)
        financial_capital = request.data.get("financial_capital", None)
        employees = request.data.get("employees", None)
        site_url = request.data.get("site_url", None)
        social_media = request.data.get("social_media", None)
        if not company_pk and not bypass_required:
            return generate_error_response("Company account primary key is required")
        if company_pk and not models.CompanyAccountModel.objects.filter(pk=company_pk).exists():
            return generate_error_response("Company account not found")
        company_obj = models.CompanyAccountModel.objects.filter(pk=company_pk).first()
        if address:
            address_list = []
            try:
                for address_json in address:
                    address_list.append(address_json)
            except Exception as e:
                return generate_error_response(f"Could not parse address JSON: {e}")
        else:
            address_list = None
        if contact and not isinstance(contact, str):
            return generate_error_response("Contact should be a String")
        if creation_date and not isinstance(creation_date, str):
            return generate_error_response("Creation date should be a String")
        if creation_date:
            try:
                formatted_creation_date = date.fromisoformat(creation_date)
            except ValueError:
                return generate_error_response("Creation date must follow the iso 8601 format (yyyy-mm-dd)")
        else:
            formatted_creation_date = None
        if financial_capital and not isinstance(financial_capital, int):
            return generate_error_response("Financial capital should be an integer")
        if employees and not isinstance(employees, int):
            return generate_error_response("Employee number should be an integer")
        if site_url and not isinstance(site_url, str):
            return generate_error_response("Site URL should be a String")
        if site_url and not str(site_url).startswith("http"):
            return generate_error_response("Site URL is not valid")
        if social_media:
            social_list = []
            try:
                for social in social_media:
                    social_list.append(social)
            except Exception as e:
                return generate_error_response(f"Could not parse social media JSON: {e}")
        else:
            social_list = None
        data = {
            "company": company_obj,
            "address": address_list,
            "contact": contact,
            "creation_date": formatted_creation_date,
            "financial_capital": financial_capital,
            "employees": employees,
            "site_url": site_url,
            "social_media": social_list
        }
        return (True, data)

    def generateManyToMany(self, profile_data, profile, just_address=False, just_social=False) -> Response | None:
        address_dict = profile_data.get("address", None)
        if address_dict is not None and not just_social:
            addresses_obj = []
            has_address_errors = False
            for addressV in address_dict:
                title = addressV.get("title", None)
                address = addressV.get("address", None)
                number = addressV.get("number", None)
                if title is None or address is None or number is None:
                    has_address_errors = True
                    continue
                if not isinstance(title, str) or not isinstance(address, str):
                    has_address_errors = True
                    continue
                try:
                    number = int(number)
                except ValueError:
                    has_address_errors = True
                    continue
                addr_obj = models.CompanyAddress.objects.create(
                    title=title,
                    address=address,
                    number=number
                )
                addresses_obj.append(addr_obj)
            if has_address_errors:
                return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                    'Issues when creating addresses from JSON. Ensure that the JSON has the format: \
                                                        [{"title":String,"address":String,"number":int}]')
            if addresses_obj:
                for addr in addresses_obj:
                    profile.address.add(addr)
                profile.save()

        social_media_dict = profile_data.get("social_media", None)
        if social_media_dict is not None and not just_address:
            social_medias_obj = []
            has_smedia_errors = False
            for smediaV in social_media_dict:
                title = smediaV.get("title", None)
                url = smediaV.get("url", None)
                username = smediaV.get("username", None)
                if title is None or url is None or username is None:
                    has_smedia_errors = True
                    continue
                if not isinstance(title, str) or not isinstance(url, str) or not isinstance(username, str):
                    has_smedia_errors = True
                    continue
                smedia_obj = models.CompanySocialMedia.objects.create(
                    title=title,
                    url=url,
                    username=username
                )
                social_medias_obj.append(smedia_obj)
            if has_smedia_errors:
                return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                    'Issues when creating social medias from JSON. Ensure that the JSON has the format: \
                                                        [{"title":String,"url":String,"username":String}]')
            if social_medias_obj:
                for smedia in social_medias_obj:
                    profile.social_media.add(smedia)
                profile.save()

        return None

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
        data_valid, data_or_response = self.handle_account_data(request, False)
        if not data_valid:
            return data_or_response
        profile_data = data_or_response
        company_obj = profile_data.get("company", None)
        contact = profile_data.get("contact", None)
        creation_date = profile_data.get("creation_date", None)
        financial_capital = profile_data.get("financial_capital", None)
        employees = profile_data.get("employees", None)
        site_url = profile_data.get("site_url", None)

        if company_obj is None:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, "Company account not found")
        if not isinstance(company_obj, models.CompanyAccountModel):
            return self.generate_basic_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Account with invalid type")

        profile = models.CompanyProfileModel(
            company_account=company_obj,
            contact=contact,
            creation_date=creation_date,
            financial_capital=financial_capital,
            employees=employees,
            site_url=site_url
        )
        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED, "Company profile created successfully")
        data = serializers.CreateCompanyProfileSerializer(profile, many=False).data
        serializer = serializers.CreateCompanyProfileSerializer(data=data)
        if serializer.is_valid():
            profile.save()
            self.generateManyToMany(profile_data, profile)
            data = serializers.CompanyProfileSerializer(profile, many=False).data
            response_data["content"] = data
            return Response(response_data, status=response_data.get("status", status.HTTP_201_CREATED))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pk = request.query_params.get("pk", None)
        if not pk:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)
        company_profile = models.CompanyProfileModel.objects.filter(pk=pk).first()
        if company_profile is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)
        data_valid, data_or_response = self.handle_account_data(request, True)
        if not data_valid:
            return data_or_response
        profile_data = data_or_response

        if profile_data.get("company", None):
            company_obj = profile_data.get("company", None)
            company_profile.company_account = company_obj
        if profile_data.get("contact", None):
            contact = profile_data.get("contact", None)
            company_profile.contact = contact
        if profile_data.get("creation_date", None):
            creation_date = profile_data.get("creation_date", None)
            company_profile.creation_date = creation_date
        if profile_data.get("financial_capital", None):
            financial_capital = profile_data.get("financial_capital", None)
            company_profile.financial_capital = financial_capital
        if profile_data.get("employees", None):
            employees = profile_data.get("employees", None)
            company_profile.employees = employees
        if profile_data.get("site_url", None):
            site_url = profile_data.get("site_url", None)
            company_profile.site_url = site_url
        if profile_data.get("address", None):
            company_profile.address.clear()
            company_profile.save()
            self.generateManyToMany(profile_data, company_profile, just_address=True)
        if profile_data.get("social_media", None):
            company_profile.social_media.clear()
            company_profile.save()
            self.generateManyToMany(profile_data, company_profile, just_social=True)
        company_profile.save()
        response_data = self.generate_basic_response_data(status.HTTP_200_OK, "Company profile patched successfully")
        serializer = serializers.CompanyProfileSerializer(company_profile)
        response_data["content"] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def delete(self, request):
        pk = request.query_params.get("pk", None)
        if not pk:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_id_str)
        company_profile = models.CompanyProfileModel.objects.filter(pk=pk).first()
        if company_profile is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_account_str)
        company_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =================== Company Authentication =================== #
class CompanyAuthSchema(AutoSchema):
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
                        'reason': 'Company logged out successfully'
                    },
                    "500": {
                        'description': 'INTERNAL SERVER ERROR',
                        'reason': 'Something went wrong'
                    }
                }
                return description_generator(title="logout a company",
                                             description=authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Company authenticated and logged in successfully'
                    },
                    "202": {
                        'description': 'ACCEPTED',
                        'reason': 'Company authenticated successfully, but, need to change password'
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
                        'reason': 'Company account not found'
                    },
                    "423": {
                        'description': 'LOCKED',
                        'reason': 'Company account can\'t be accessed due to a ban or other issue'
                    },
                    "500": {
                        'description': 'INTERNAL SERVER ERROR',
                        'reason': 'Something went wrong'
                    }
                }
                return description_generator(title="Authenticate and login a company",
                                             description=authorization_info,
                                             responses=responses)
            case _:
                return ''

    def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
        match method:
            case 'POST':
                return [
                    coreapi.Field(
                        name="cnpj",
                        location="form",
                        required=True,
                        schema=coreschema.String(15),
                        description="Company cnpj"
                    ),
                    coreapi.Field(
                        name="password",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Company's account password"
                    )
                ]
            case _:
                return []


class CompanyAuth(Base):
    schema = CompanyAuthSchema()

    def get(self, request):
        return self.generate_basic_response(status.HTTP_200_OK, "Logged out")

    def post(self, request):
        cnpj = request.data.get('cnpj', None)
        password = request.data.get('password', None)

        if cnpj is None or password is None:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                "CNPJ or password not found")

        if not CNPJ().validar(str(cnpj)):
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                "Invalid CNPJ")

        company = models.CompanyAccountModel.objects.filter(cnpj=cnpj, password=password).first()

        if company is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                "No account found with this CNPJ")

        profile = models.CompanyProfileModel.objects.filter(company_account=company).first()

        if profile is None:
            return self.generate_basic_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                "Company profile not found")

        if company.banned:
            return self.generate_basic_response(status.HTTP_423_LOCKED,
                                                "Company's account is banned")

        if company.should_change_password:
            data = self.generate_basic_response_data(status.HTTP_202_ACCEPTED,
                                                     "Company must change password before logging in")
            serializer = serializers.CompanyProfileSerializer(profile)
            data['content'] = serializer.data
            return Response(data=data, status=data.get('status', status.HTTP_202_ACCEPTED))

        data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                 "Logged in successfully")
        serializer = serializers.CompanyProfileSerializer(profile)
        data['content'] = serializer.data
        return Response(data=data, status=data.get('status', status.HTTP_200_OK))
