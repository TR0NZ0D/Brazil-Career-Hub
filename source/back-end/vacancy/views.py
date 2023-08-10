import coreapi
import coreschema

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from api.tools.api_tools import description_generator
from api.views import Base
from .serializers import VacancyModelSerializer
from . import models


# =================== Vacancy =================== #
class VacancySchema(AutoSchema):
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

Inform PK if mentioning specific vacancy

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Vacancy found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Vacancy not found'
                    }
                }
                return description_generator(title="Get a specific vacancy or all vacancies",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Vacancy successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a vacancy",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Vacancy successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Vacancy ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from vacancy",
                                             # noqa: E502
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Vacancy successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Vacancy not found'
                    }
                }
                return description_generator(title="Delete a specific vacancy",
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
                        description="Vacancy ID"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="role",
                        location="form",
                        required=True,
                        schema=coreschema.String(255),
                        description="Vacancy role (or title)"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Vacancy description"
                    ),
                    coreapi.Field(
                        name="modality",
                        location='form',
                        required=True,
                        schema=coreschema.String(255),
                        description="Vacancy modality"
                    ),
                    coreapi.Field(
                        name="salary",
                        location='form',
                        required=True,
                        schema=coreschema.Integer(),
                        description="Vacancy salary"
                    ),
                    coreapi.Field(
                        name="address",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(255)),
                        description="Vacancy address (JSON should contain two strings and an integer)"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Vacancy ID"
                    ),
                    coreapi.Field(
                        name="role",
                        location="form",
                        required=False,
                        schema=coreschema.String(255),
                        description="Vacancy role (or title)"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Vacancy description"
                    ),
                    coreapi.Field(
                        name="modality",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Vacancy modality"
                    ),
                    coreapi.Field(
                        name="salary",
                        location='form',
                        required=False,
                        schema=coreschema.Integer(),
                        description="Vacancy salary"
                    ),
                    coreapi.Field(
                        name="address",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.String(255)),
                        description="Vacancy address (JSON should contain two strings and an integer)"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Vacancy ID"
                    )
                ]
            case _:
                return []


class Vacancy(Base):
    schema = VacancySchema()

    not_found_id_str = "Vacancy ID not found"
    not_found_vacancy_str = "Vacancy not found"

    def handle_vacancy_data(self, request, bypass_required):
        def generate_error_response(text: str):
            return (False, self.generate_basic_response(status.HTTP_400_BAD_REQUEST, text))
        # Required
        role = request.data.get("role", None)
        description = request.data.get("description", None)
        modality = request.data.get("modality", None)
        salary = request.data.get("salary", None)
        # Optionals
        address = request.data.get("address", None)

        # Role validations
        if role is None and not bypass_required:
            return generate_error_response("Role is required")

        if role and not isinstance(role, str):
            return generate_error_response("Role should be a string")

        if role and len(role) > 255:
            return generate_error_response("Role should have a max length of 255 characters")

        # Description validation
        if description is None and not bypass_required:
            return generate_error_response("Description is required")

        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Modality validation
        if modality is None and not bypass_required:
            return generate_error_response("Modality is required")

        if modality and not isinstance(modality, str):
            return generate_error_response("Modality should be a string")

        if modality and len(modality) > 255:
            return generate_error_response("Modality should have a max length of 255 characters")

        # Salary validations
        if salary is None and not bypass_required:
            return generate_error_response("Salary is required")

        if salary and not isinstance(salary, int):
            return generate_error_response("Salary should be an integer")

        if salary and salary < 0:
            return generate_error_response("Salary should be a positive integer")

        # Address validations
        if not isinstance(address, dict):
            return generate_error_response("Could not parse address JSON: address is not a json-like object")

        if address and (not address.get("title") or not address.get("address") or not address.get("number")):
            return generate_error_response("Could not parse address JSON: missing required address fields")

        data = {
            "role": role,
            "description": description,
            "modality": modality,
            "salary": salary,
            "address": address
        }

        return (True, data)

    def get(self, request):
        """Get request"""
        primary_key = request.query_params.get('pk', None)

        if primary_key:
            vacancy = models.VacancyModel.objects.all().filter(pk=primary_key).first()

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "")
            if vacancy is not None:
                serializer = VacancyModelSerializer(vacancy)
                response_data['content'] = serializer.data
                return Response(data=response_data, status=status.HTTP_200_OK)

            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_vacancy_str)

        vacancies = models.VacancyModel.objects.all()

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "")

        if vacancies is not None:
            serializer = VacancyModelSerializer(vacancies, many=True)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        response_data['content'] = []
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request):
        data_valid, data_or_response = self.handle_vacancy_data(request, False)
        if not data_valid:
            return data_or_response
        vacancy_data = data_or_response
        role = vacancy_data.get("role", "")
        description = vacancy_data.get("description", "")
        modality = vacancy_data.get("modality", "")
        salary = vacancy_data.get("salary", 0)
        address = vacancy_data.get("address", {})

        address_model = models.VacancyAddress.objects.create(
            title=address.get('title', ''),
            address=address.get('address', ''),
            number=address.get('number', 0)
        )

        vacancy = models.VacancyModel(
            role=role,
            description=description,
            modality=modality,
            salary=salary,
            address=address_model
        )
        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED, "Vacancy created successfully")
        data = VacancyModelSerializer(vacancy, many=False).data
        serializer = VacancyModelSerializer(data=data)
        if serializer.is_valid():
            vacancy.save()
            data = VacancyModelSerializer(vacancy, many=False).data
            response_data["content"] = data
            return Response(response_data, status=response_data.get("status", status.HTTP_201_CREATED))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        primary_key = request.query_params.get('pk', None)

        if not primary_key:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_id_str)

        vacancy = models.VacancyModel.objects.all().filter(pk=primary_key).first()

        if vacancy is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_vacancy_str)

        data_valid, data_or_response = self.handle_vacancy_data(request, True)
        if not data_valid:
            return data_or_response
        vacancy_data = data_or_response

        if vacancy_data.get("role", None):
            role = vacancy_data.get("role", "")
            vacancy.role = role
        if vacancy_data.get("description", None):
            description = vacancy_data.get("description", "")
            vacancy.description = description
        if vacancy_data.get("modality", None):
            modality = vacancy_data.get("modality", "")
            vacancy.modality = modality
        if vacancy_data.get("salary", None):
            salary = vacancy_data.get("salary", 0)
            vacancy.salary = salary
        if vacancy_data.get("address", None):
            address = vacancy_data.get("address", {})
            address_model = models.VacancyAddress.objects.create(
                title=address.get('title', ''),
                address=address.get('address', ''),
                number=address.get('number', 0)
            )
            vacancy.address = address_model

        try:
            vacancy.clean_fields()
            vacancy.clean()
        except ValidationError as error:
            data = self.generate_basic_response_data(status.HTTP_400_BAD_REQUEST, "Patch data validation error")
            data["errors"] = error
            return Response(data=data, status=data.get("status"))

        vacancy.save()
        response_data = self.generate_basic_response_data(status.HTTP_200_OK, "Vacancy patched successfully")
        serializer = VacancyModelSerializer(vacancy)
        response_data["content"] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def delete(self, request):
        primary_key = request.query_params.get('pk', None)

        if not primary_key:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_id_str)

        vacancy = models.VacancyModel.objects.all().filter(pk=primary_key).first()

        if vacancy is not None:
            vacancy.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_vacancy_str)
