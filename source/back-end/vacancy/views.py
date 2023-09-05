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

from company.models import CompanyProfileModel
from resumes.models import ResumeModel


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
Inform company_pk to get all vacancies from that company (company account ID)

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Vacancy found'
                    },
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'No vacancies found for the specific company'
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
                        'reason': 'Vacancy ID or Resume ID not found'
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
                    ),
                    coreapi.Field(
                        name="company_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Company account ID (all vacancies)"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="created_by",
                        location="form",
                        required=True,
                        schema=coreschema.Integer(),
                        description="Company account ID"
                    ),
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
                        name="created_by",
                        location="form",
                        required=False,
                        schema=coreschema.Integer(),
                        description="Company account ID"
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
                    ),
                    coreapi.Field(
                        name="resumes",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Integer()),
                        description="Vacancy resumes PK (add or remove resume)"
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
        created_by = request.data.get("created_by", None)
        role = request.data.get("role", None)
        description = request.data.get("description", None)
        modality = request.data.get("modality", None)
        salary = request.data.get("salary", None)
        # Optionals
        address = request.data.get("address", None)
        resumes = request.data.get("resumes", None)

        # Company account validations
        if created_by is None and not bypass_required:
            return generate_error_response("Company ID is required")

        if created_by and not isinstance(created_by, int):
            return generate_error_response("created_by should be an integer (Company account ID)")

        if created_by:
            try:
                company_pk = int(created_by)
                company = CompanyProfileModel.objects.filter(company_account__pk=company_pk).first()
                if company is None:
                    return generate_error_response(f"Company with PK {company_pk} not found")
            except Exception as e:
                return generate_error_response(f"Invalid account ID: {e}")
        else:
            company = None

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
        if address and not isinstance(address, dict):
            return generate_error_response("Could not parse address JSON: address is not a json-like object")

        if address and (not address.get("title") or not address.get("address") or not address.get("number")):
            return generate_error_response("Could not parse address JSON: missing required address fields")

        # Resumes validations
        if resumes and not isinstance(resumes, list):
            return generate_error_response("Resumes should be an array")

        if resumes:
            resume_array: list[ResumeModel] = []
            for resume in resumes:
                if not isinstance(resume, int):
                    try:
                        return generate_error_response(f"Resume pk {resume} in index {resumes.index(resume)} should be an integer")
                    except Exception:
                        return generate_error_response("Resume array is invalid")

                res_obj = ResumeModel.objects.filter(pk=resume).first()

                if res_obj is None:
                    return generate_error_response(f"Resume pk {resume} in index {resumes.index(resume)} could not be found")

                resume_array.append(res_obj)
        else:
            resume_array: list[ResumeModel] = []

        data = {
            "created_by": company,
            "role": role,
            "description": description,
            "modality": modality,
            "salary": salary,
            "address": address,
            "resumes": resume_array
        }

        return (True, data)

    def get(self, request):
        """Get request"""
        primary_key = request.query_params.get('pk', None)

        if primary_key:
            vacancy = models.VacancyModel.objects.all().filter(pk=primary_key).first()

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Vacancy found")
            if vacancy is not None:
                serializer = VacancyModelSerializer(vacancy)
                response_data['content'] = serializer.data
                return Response(data=response_data, status=status.HTTP_200_OK)

            return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_vacancy_str)

        company_pk = request.query_params.get('company_pk', None)

        if company_pk:
            company_vacancies = models.VacancyModel.objects.filter(created_by__pk=company_pk)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Vacancies found")

            if company_vacancies:
                serializer = VacancyModelSerializer(company_vacancies, many=True)
                response_data['content'] = serializer.data
                return Response(data=response_data, status=status.HTTP_200_OK)

            return self.generate_basic_response(status.HTTP_204_NO_CONTENT, "No vacancies found for this company")

        vacancies = models.VacancyModel.objects.all()

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Vacancies found")

        if vacancies is not None:
            serializer = VacancyModelSerializer(vacancies, many=True)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND, self.not_found_vacancy_str)

    def post(self, request):
        data_valid, data_or_response = self.handle_vacancy_data(request, False)
        if not data_valid:
            return data_or_response
        vacancy_data = data_or_response
        created_by = vacancy_data.get("created_by", None)
        role = vacancy_data.get("role", "")
        description = vacancy_data.get("description", "")
        modality = vacancy_data.get("modality", "")
        salary = vacancy_data.get("salary", 0)
        address = vacancy_data.get("address", {})

        if address:
            address_model = models.VacancyAddress.objects.create(
                title=address.get('title', ''),
                address=address.get('address', ''),
                number=address.get('number', 0)
            )
        else:
            address_model = None

        vacancy = models.VacancyModel(
            created_by=created_by.company_account,
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

        if vacancy_data.get("created_by", None):
            created_by = vacancy_data.get("created_by", None)
            vacancy.created_by = created_by
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
        if vacancy_data.get("resumes", None) is not None:
            vacancy.resumes.clear()
            vacancy.save()

            resumes = vacancy_data.get("resumes", [])
            for resume in resumes:
                vacancy.resumes.add(resume)

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
