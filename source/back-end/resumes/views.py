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
from typing import Any


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
    def get_resume(request: HttpRequest) -> models.ResumeModel | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeModel.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_resumes(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeModel.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeModel.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeModel.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_resume(request: HttpRequest) -> models.ResumeModel:
        pass

    @staticmethod
    def edit_resume(request: HttpRequest, resume: models.ResumeModel):
        pass

    @staticmethod
    def delete_resume(request: HttpRequest, resume: models.ResumeModel):
        resume_model = ResumeTools.get_resume(request)

        if resume_model is None:
            return

        if resume_model.pk != resume.pk:
            return

        resume.delete()

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
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform resume PK if mentioning specific resume
- Inform user pk / profile pk / profile slug to get all resumes

"""

        unique_query_params_info = """
## Query Parameters

Inform resume PK if mentioning specific resume

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Resume found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Resume not found'
                    }
                }
                return description_generator(title="Get a specific resume or all resumes from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Resume successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a resume",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Resume successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Resume ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from resume",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Resume successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Resume not found'
                    }
                }
                return description_generator(title="Delete a specific resume",
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
                        description="Resume ID (returns specific resume)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all resumes)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all resumes)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all resumes)"
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
                        description="Resume title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Resume description"
                    ),
                    coreapi.Field(
                        name="experiences",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Experiences dict or PK"
                    ),
                    coreapi.Field(
                        name="competencies",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Competencies dict or PK"
                    ),
                    coreapi.Field(
                        name="courses",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Courses dict or PK"
                    ),
                    coreapi.Field(
                        name="references",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="References dict or PK"
                    ),
                    coreapi.Field(
                        name="graduations",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Graduations dict or PK"
                    ),
                    coreapi.Field(
                        name="projects",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Projects dict or PK"
                    ),
                    coreapi.Field(
                        name="links",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Links dict or PK"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Resume ID"
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
                        description="Resume title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Resume description"
                    ),
                    coreapi.Field(
                        name="experiences",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Experiences dict or PK"
                    ),
                    coreapi.Field(
                        name="competencies",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Competencies dict or PK"
                    ),
                    coreapi.Field(
                        name="courses",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Courses dict or PK"
                    ),
                    coreapi.Field(
                        name="references",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="References dict or PK"
                    ),
                    coreapi.Field(
                        name="graduations",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Graduations dict or PK"
                    ),
                    coreapi.Field(
                        name="projects",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Projects dict or PK"
                    ),
                    coreapi.Field(
                        name="links",
                        location='form',
                        required=False,
                        schema=coreschema.Object(),
                        description="Links dict or PK"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Resume ID"
                    )
                ]
            case _:
                return []


class Resume(Base):
    schema = ResumeSchema()

    not_found_id_str = "Resume ID not found"
    not_found_resume_str = "Resume not found"

    def get(self, request, *args, **kwargs):

        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            resume_model: models.ResumeModel | None = ResumeTools.get_resume(request)

            if resume_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_resume_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Resume found")

            serializer = serializers.ResumeModelSerializer(resume_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        resume_models: Any | None = ResumeTools.get_all_resumes(request)

        if resume_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_resume_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Resumes found")

        serializer = serializers.ResumeModelSerializer(resume_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        resume_model = ResumeTools.get_resume(request)

        if resume_model is not None:
            ResumeTools.delete_resume(request, resume_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_resume_str)


# ========== Experience ========== #
class ExperienceSchema(AutoSchema):
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform experience PK if mentioning specific experience
- Inform user pk / profile pk / profile slug to get all experiencies

"""

        unique_query_params_info = """
## Query Parameters

Inform experience PK if mentioning specific experience

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Experience found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Experience not found'
                    }
                }
                return description_generator(title="Get a specific experience or all experiencies from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Experience successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a experience",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Experience successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Experience ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from experience",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Experience successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Experience not found'
                    }
                }
                return description_generator(title="Delete a specific experience",
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
                        description="Link ID (returns specific experience)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all experiencies)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all experiencies)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all experiencies)"
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
                        description="Experience title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience item description"
                    ),
                    coreapi.Field(
                        name="experience_company",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience company"
                    ),
                    coreapi.Field(
                        name="experience_role",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience role"
                    ),
                    coreapi.Field(
                        name="experience_description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience description"
                    ),
                    coreapi.Field(
                        name="experience_start_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience start date (ISO format)"
                    ),
                    coreapi.Field(
                        name="experience_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience end date (ISO format)"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Experience ID"
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
                        description="Experience title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience item description"
                    ),
                    coreapi.Field(
                        name="experience_company",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience company"
                    ),
                    coreapi.Field(
                        name="experience_role",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience role"
                    ),
                    coreapi.Field(
                        name="experience_description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience description"
                    ),
                    coreapi.Field(
                        name="experience_start_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience start date (ISO format)"
                    ),
                    coreapi.Field(
                        name="experience_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience end date (ISO format)"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Experience ID"
                    )
                ]
            case _:
                return []


class Experience(Base):
    schema = ExperienceSchema()

    not_found_id_str = "Experience ID not found"
    not_found_experience_str = "Experience not found"

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
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform competence PK if mentioning specific competence
- Inform user pk / profile pk / profile slug to get all competencies

"""

        unique_query_params_info = """
## Query Parameters

Inform competence PK if mentioning specific competence

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Competence found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Competence not found'
                    }
                }
                return description_generator(title="Get a specific competence or all competencies from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Competence successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a competence",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Competence successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Competence ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from competence",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Competence successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Competence not found'
                    }
                }
                return description_generator(title="Delete a specific competence",
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
                        description="Link ID (returns specific competence)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all competencies)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all competencies)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all competencies)"
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
                        description="Competence title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Competence description"
                    ),
                    coreapi.Field(
                        name="competence_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Competence name"
                    ),
                    coreapi.Field(
                        name="competence_level",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Competence level"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Competence ID"
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
                        description="Competence title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Competence description"
                    ),
                    coreapi.Field(
                        name="competence_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Competence name"
                    ),
                    coreapi.Field(
                        name="competence_level",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Competence level"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Competence ID"
                    )
                ]
            case _:
                return []


class Competence(Base):
    schema = CompetenceSchema()

    not_found_id_str = "Competence ID not found"
    not_found_competence_str = "Competence not found"

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
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform course PK if mentioning specific course
- Inform user pk / profile pk / profile slug to get all courses

"""

        unique_query_params_info = """
## Query Parameters

Inform course PK if mentioning specific course

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Course found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Course not found'
                    }
                }
                return description_generator(title="Get a specific course or all courses from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Course successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a course",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Course successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Course ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from course",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Course successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Course not found'
                    }
                }
                return description_generator(title="Delete a specific course",
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
                        description="Course ID (returns specific course)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all courses)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all courses)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all courses)"
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
                        description="Course title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course description"
                    ),
                    coreapi.Field(
                        name="course_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course name"
                    ),
                    coreapi.Field(
                        name="course_locale",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course locale"
                    ),
                    coreapi.Field(
                        name="course_provider",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course provider"
                    ),
                    coreapi.Field(
                        name="course_hours",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course hours"
                    ),
                    coreapi.Field(
                        name="course_start_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course start date (ISO format)"
                    ),
                    coreapi.Field(
                        name="course_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course end date (ISO format)"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Course ID"
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
                        description="Course title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course description"
                    ),
                    coreapi.Field(
                        name="course_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course name"
                    ),
                    coreapi.Field(
                        name="course_locale",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course locale"
                    ),
                    coreapi.Field(
                        name="course_provider",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course provider"
                    ),
                    coreapi.Field(
                        name="course_hours",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course hours"
                    ),
                    coreapi.Field(
                        name="course_start_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course start date (ISO format)"
                    ),
                    coreapi.Field(
                        name="course_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course end date (ISO format)"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Course ID"
                    )
                ]
            case _:
                return []


class Course(Base):
    schema = CourseSchema()

    not_found_id_str = "Course ID not found"
    not_found_course_str = "Course not found"

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
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform reference PK if mentioning specific reference
- Inform user pk / profile pk / profile slug to get all references

"""

        unique_query_params_info = """
## Query Parameters

Inform reference PK if mentioning specific reference

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Reference found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Reference not found'
                    }
                }
                return description_generator(title="Get a specific reference or all references from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Reference successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a reference",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Reference successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Reference ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from reference",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Reference successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Reference not found'
                    }
                }
                return description_generator(title="Delete a specific Reference",
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
                        description="Reference ID (returns specific reference)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all references)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all references)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all references)"
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
                        description="Reference title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference description"
                    ),
                    coreapi.Field(
                        name="reference_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference name"
                    ),
                    coreapi.Field(
                        name="reference_role",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference role"
                    ),
                    coreapi.Field(
                        name="reference_company",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference company"
                    ),
                    coreapi.Field(
                        name="reference_phone",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference phone"
                    ),
                    coreapi.Field(
                        name="refecence_email",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference email"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Reference ID"
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
                        description="Reference title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference description"
                    ),
                    coreapi.Field(
                        name="reference_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference name"
                    ),
                    coreapi.Field(
                        name="reference_role",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference role"
                    ),
                    coreapi.Field(
                        name="reference_company",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference company"
                    ),
                    coreapi.Field(
                        name="reference_phone",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference phone"
                    ),
                    coreapi.Field(
                        name="refecence_email",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Reference email"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Reference ID"
                    )
                ]
            case _:
                return []


class Reference(Base):
    schema = ReferenceSchema()

    not_found_id_str = "Reference ID not found"
    not_found_reference_str = "Reference not found"

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
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform graduation PK if mentioning specific graduation
- Inform user pk / profile pk / profile slug to get all graduations

"""

        unique_query_params_info = """
## Query Parameters

Inform graduation PK if mentioning specific graduation

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Graduation found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Graduation not found'
                    }
                }
                return description_generator(title="Get a specific graduation or all graduations from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Graduation successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a graduation",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Graduation successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Graduation ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from graduation",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Graduation successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Graduation not found'
                    }
                }
                return description_generator(title="Delete a specific graduation",
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
                        description="Graduation ID (returns specific graduation)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all graduations)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all graduations)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all graduations)"
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
                        description="Graduation title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation description"
                    ),
                    coreapi.Field(
                        name="graduation_type",
                        location='form',
                        required=False,
                        schema=coreschema.String(150),
                        description="Graduation Type"
                    ),
                    coreapi.Field(
                        name="graduation_period",
                        location='form',
                        required=False,
                        schema=coreschema.String(150),
                        description="Graduation Period (hours)"
                    ),
                    coreapi.Field(
                        name="graduation_start_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation start date (ISO format)"
                    ),
                    coreapi.Field(
                        name="graduation_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation end date (ISO format)"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Graduation ID"
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
                        description="Graduation title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation description"
                    ),
                    coreapi.Field(
                        name="graduation_type",
                        location='form',
                        required=False,
                        schema=coreschema.String(150),
                        description="Graduation Type"
                    ),
                    coreapi.Field(
                        name="graduation_period",
                        location='form',
                        required=False,
                        schema=coreschema.String(150),
                        description="Graduation Period (hours)"
                    ),
                    coreapi.Field(
                        name="graduation_start_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation start date (ISO format)"
                    ),
                    coreapi.Field(
                        name="graduation_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation end date (ISO format)"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Graduation ID"
                    )
                ]
            case _:
                return []


class Graduation(Base):
    schema = GraduationSchema()

    not_found_id_str = "Graduation ID not found"
    not_found_graduation_str = "Graduation not found"

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
    def get_description(self, path: str, method: str) -> str:
        authorization_info = """
## Authorization:

**Type:** Bearer
"""

        query_params_info = """
## Query Parameters

- Inform project PK if mentioning specific project
- Inform user pk / profile pk / profile slug to get all projects

"""

        unique_query_params_info = """
## Query Parameters

Inform project PK if mentioning specific project

"""

        match method:
            case 'GET':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Project found'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Project not found'
                    }
                }
                return description_generator(title="Get a specific project or all project from a specific user",
                                             description=query_params_info + authorization_info,
                                             responses=responses)
            case 'POST':
                responses = {
                    "201": {
                        'description': 'CREATED',
                        'reason': 'Project successfully created'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Create a project",
                                             description=authorization_info,
                                             responses=responses)
            case 'PATCH':
                responses = {
                    "200": {
                        'description': 'OK',
                        'reason': 'Project successfully updated'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Project ID not found'
                    },
                    "400": {
                        'description': "BAD REQUEST",
                        'reason': 'Invalid request body'
                    }
                }
                return description_generator(title="Update specific information from project",
                                             # noqa: E502
                                             description=unique_query_params_info + authorization_info,
                                             responses=responses)
            case 'DELETE':
                responses = {
                    "204": {
                        'description': 'NO CONTENT',
                        'reason': 'Project successfully deleted'
                    },
                    "404": {
                        'description': 'NOT FOUND',
                        'reason': 'Project not found'
                    }
                }
                return description_generator(title="Delete a specific project",
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
                        description="Project ID (returns specific project)"
                    ),
                    coreapi.Field(
                        name="user_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="User ID (return all projects)"
                    ),
                    coreapi.Field(
                        name="profile_pk",
                        location="query",
                        required=False,
                        schema=coreschema.Integer(minimum=1),
                        description="Profile ID (return all projects)"
                    ),
                    coreapi.Field(
                        name="slug",
                        location="query",
                        required=False,
                        schema=coreschema.String(),
                        description="Profile slug (return all projects)"
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
                        description="Project title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Project item description"
                    ),
                    coreapi.Field(
                        name="project_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Project name"
                    ),
                    coreapi.Field(
                        name="project_description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Project description"
                    ),
                    coreapi.Field(
                        name="project_link",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Project URL"
                    )
                ]
            case 'PATCH':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Project ID"
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
                        description="Project title"
                    ),
                    coreapi.Field(
                        name="description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Project item description"
                    ),
                    coreapi.Field(
                        name="project_name",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Project name"
                    ),
                    coreapi.Field(
                        name="project_description",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Project description"
                    ),
                    coreapi.Field(
                        name="project_link",
                        location='form',
                        required=False,
                        schema=coreschema.String(255),
                        description="Project URL"
                    )
                ]
            case 'DELETE':
                return [
                    coreapi.Field(
                        name="pk",
                        location="query",
                        required=True,
                        schema=coreschema.Integer(minimum=1),
                        description="Project ID"
                    )
                ]
            case _:
                return []


class Project(Base):
    schema = ProjectSchema()

    not_found_id_str = "Project ID not found"
    not_found_project_str = "Project not found"

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
                        required=False,
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
    not_found_link_str = "Link not found"

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
