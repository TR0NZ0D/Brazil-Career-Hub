import coreapi
import coreschema

from django.http import HttpRequest
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from api.tools.api_tools import description_generator
from api.views import Base
from . import serializers
from . import models
from users.models import UserProfile
from users.serializers import UserProfileSerializer


# ========== Generics ========== #
class ResumeTools:
    # ====== Generics ====== #
    @staticmethod
    def get_resume_data(request: HttpRequest, bypass_required: bool):
        pass

    @staticmethod
    def get_experience_data(request: HttpRequest, bypass_required: bool):
        pass

    @staticmethod
    def get_competence_data(request: HttpRequest, bypass_required: bool):
        pass

    @staticmethod
    def get_course_data(request: HttpRequest, bypass_required: bool):
        pass

    @staticmethod
    def get_reference_data(request: HttpRequest, bypass_required: bool):
        pass

    @staticmethod
    def get_graduation_data(request: HttpRequest, bypass_required: bool):
        pass

    @staticmethod
    def get_project_data(request: HttpRequest, bypass_required: bool):
        pass

    @staticmethod
    def get_link_data(request: HttpRequest, bypass_required: bool):
        pass

    # ====== Resume ====== #
    @staticmethod
    def get_resume(request: HttpRequest) -> models.ResumeModel | list[models.ResumeModel] | None:
        pass

    @staticmethod
    def create_resume(request: HttpRequest) -> models.ResumeModel:
        pass

    @staticmethod
    def edit_resume(request: HttpRequest, resume: models.ResumeModel):
        pass

    @staticmethod
    def delete_resume(request: HttpRequest, resume: models.ResumeModel):
        pass

    @staticmethod
    def add_experience_to_resume(request: HttpRequest, resume: models.ResumeModel, experience: models.ResumeExperience):
        pass

    @staticmethod
    def add_competence_to_resume(request: HttpRequest, resume: models.ResumeModel, competence: models.ResumeCompetence):
        pass

    @staticmethod
    def add_course_to_resume(request: HttpRequest, resume: models.ResumeModel, course: models.ResumeCourse):
        pass

    @staticmethod
    def add_reference_to_resume(request: HttpRequest, resume: models.ResumeModel, reference: models.ResumeReference):
        pass

    @staticmethod
    def add_graduation_to_resume(request: HttpRequest, resume: models.ResumeModel, graduation: models.ResumeGraduation):
        pass

    @staticmethod
    def add_project_to_resume(request: HttpRequest, resume: models.ResumeModel, project: models.ResumeProject):
        pass

    @staticmethod
    def add_link_to_resume(request: HttpRequest, resume: models.ResumeModel, link: models.ResumeLink):
        pass

    # ====== Experience ====== #
    @staticmethod
    def get_experience(request: HttpRequest) -> models.ResumeExperience | list[models.ResumeExperience] | None:
        pass

    @staticmethod
    def create_experience(request: HttpRequest) -> models.ResumeExperience:
        pass

    @staticmethod
    def edit_experience(request: HttpRequest, experience: models.ResumeExperience):
        pass

    @staticmethod
    def delete_experience(request: HttpRequest, experience: models.ResumeExperience):
        pass

    # ====== Competence ====== #
    @staticmethod
    def get_competence(request: HttpRequest) -> models.ResumeCompetence | list[models.ResumeCompetence] | None:
        pass

    @staticmethod
    def create_competence(request: HttpRequest) -> models.ResumeCompetence:
        pass

    @staticmethod
    def edit_competence(request: HttpRequest, competence: models.ResumeCompetence):
        pass

    @staticmethod
    def delete_competence(request: HttpRequest, competence: models.ResumeCompetence):
        pass

    # ====== Course ====== #
    @staticmethod
    def get_course(request: HttpRequest) -> models.ResumeCourse | list[models.ResumeCourse] | None:
        pass

    @staticmethod
    def create_course(request: HttpRequest) -> models.ResumeCourse:
        pass

    @staticmethod
    def edit_course(request: HttpRequest, course: models.ResumeCourse):
        pass

    @staticmethod
    def delete_course(request: HttpRequest, course: models.ResumeCourse):
        pass

    # ====== Reference ====== #
    @staticmethod
    def get_reference(request: HttpRequest) -> models.ResumeReference | list[models.ResumeReference] | None:
        pass

    @staticmethod
    def create_reference(request: HttpRequest) -> models.ResumeReference:
        pass

    @staticmethod
    def edit_reference(request: HttpRequest, reference: models.ResumeReference):
        pass

    @staticmethod
    def delete_reference(request: HttpRequest, reference: models.ResumeReference):
        pass

    # ====== Graduation ====== #
    @staticmethod
    def get_graduation(request: HttpRequest) -> models.ResumeGraduation | list[models.ResumeGraduation] | None:
        pass

    @staticmethod
    def create_graduation(request: HttpRequest) -> models.ResumeGraduation:
        pass

    @staticmethod
    def edit_graduation(request: HttpRequest, graduation: models.ResumeGraduation):
        pass

    @staticmethod
    def delete_graduation(request: HttpRequest, graduation: models.ResumeGraduation):
        pass

    # ====== Project ====== #
    @staticmethod
    def get_project(request: HttpRequest) -> models.ResumeProject | list[models.ResumeProject] | None:
        pass

    @staticmethod
    def create_project(request: HttpRequest) -> models.ResumeProject:
        pass

    @staticmethod
    def edit_project(request: HttpRequest, project: models.ResumeProject):
        pass

    @staticmethod
    def delete_project(request: HttpRequest, project: models.ResumeProject):
        pass

    # ====== Link ====== #
    @staticmethod
    def get_link(request: HttpRequest) -> models.ResumeLink | list[models.ResumeLink] | None:
        pass

    @staticmethod
    def create_link(request: HttpRequest) -> models.ResumeLink:
        pass

    @staticmethod
    def edit_link(request: HttpRequest, link: models.ResumeLink):
        pass

    @staticmethod
    def delete_link(request: HttpRequest, link: models.ResumeLink):
        pass


# ========== Resume ========== #
class ResumeSchema(AutoSchema):
    # TODO: Edit to resume
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


class Resume(Base):
    schema = ResumeSchema()

    not_found_id_str = "Resume ID not found"
    not_found_vacancy_str = "Resume not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


# ========== Experience ========== #
class ExperienceSchema(AutoSchema):
    # TODO: Edit to experience
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


class Experience(Base):
    schema = ExperienceSchema()

    not_found_id_str = "Experience ID not found"
    not_found_vacancy_str = "Experience not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


# ========== Competence ========== #
class CompetenceSchema(AutoSchema):
    # TODO: Edit to competence
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


class Competence(Base):
    schema = CompetenceSchema()

    not_found_id_str = "Competence ID not found"
    not_found_vacancy_str = "Competence not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


# ========== Course ========== #
class CourseSchema(AutoSchema):
    # TODO: Edit to course
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


class Course(Base):
    schema = CourseSchema()

    not_found_id_str = "Course ID not found"
    not_found_vacancy_str = "Course not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


# ========== Reference ========== #
class ReferenceSchema(AutoSchema):
    # TODO: Edit to reference
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


class Reference(Base):
    schema = ReferenceSchema()

    not_found_id_str = "Reference ID not found"
    not_found_vacancy_str = "Reference not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


# ========== Graduation ========== #
class GraduationSchema(AutoSchema):
    # TODO: Edit to graduation
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


class Graduation(Base):
    schema = GraduationSchema()

    not_found_id_str = "Graduation ID not found"
    not_found_vacancy_str = "Graduation not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


# ========== Project ========== #
class ProjectSchema(AutoSchema):
    # TODO: Edit to project
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


class Project(Base):
    schema = ProjectSchema()

    not_found_id_str = "Project ID not found"
    not_found_vacancy_str = "Project not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


# ========== Link ========== #
class LinkSchema(AutoSchema):
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform link PK if mentioning specific link
- Inform user pk / profile pk / profile slug to get all links

"""

        unique_query_params_info = """
## Query Parameters

Inform link PK if mentioning specific link

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Link found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Link not found'
                    }
                }
                return description_generator(title="Get a specific link or all links from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Link successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a link",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Link successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Link ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from link",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Link successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Link not found'
                    }
                }
                return description_generator(title="Delete a specific link",
                                             description=unique_query_params_info + authorization_info,
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
                        description="Link ID (returns specific link)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all links)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all links)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all links)"
                    )
                ]
            case 'POST':
                return [
                    coreapi.Field(
                        name="profile_pk",
                        location="form",
                        required=True,
                        schema=coreschema.Integer(),
                        description="Profile ID"
                    ),
                    coreapi.Field(
                        name="title",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Link title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Link description"
                    ),
                    coreapi.Field(
                        name="url",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Link URL"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Link ID"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="form",
                        required=False,
                        schema=coreschema.Integer(),
                        description="Profile ID"
                    ),
                    coreapi.Field(
                        name="title",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Link title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Link description"
                    ),
                    coreapi.Field(
                        name="url",
                        location='form',
                        required=True,
                        schema=coreschema.String(),
                        description="Link URL"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Link ID"
                    )
                ]
            case _:
                return []


class Link(Base):
    schema = LinkSchema()

    not_found_id_str = "Link ID not found"
    not_found_vacancy_str = "Link not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
