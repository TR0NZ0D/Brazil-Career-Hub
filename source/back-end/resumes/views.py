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
from datetime import datetime


# ========== Generics ========== #
class ResumeTools:
    # ====== Generic Validations ====== #
    @staticmethod
    def validate_date(date: str):
        pass

    # ====== Generics ====== #
    @staticmethod
    def get_resume_data(request: HttpRequest, bypass_required: bool) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        # required
        profile_pk = request.data.get("profile_pk", None)  # type: ignore

        # optional
        title = request.data.get("title", None)  # type: ignore
        description = request.data.get("description", None)  # type: ignore
        experiences = request.data.get("experiences", None)  # type: ignore
        competencies = request.data.get("competencies", None)  # type: ignore
        courses = request.data.get("courses", None)  # type: ignore
        references = request.data.get("references", None)  # type: ignore
        graduations = request.data.get("graduations", None)  # type: ignore
        projects = request.data.get("projects", None)  # type: ignore
        links = request.data.get("links", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Experience validations
        if experiences and not isinstance(experiences, list):
            return generate_error_response("Experiences should be an array")

        is_experiences_dict = False
        is_experiences_pk = False
        is_experiences_both = False
        if experiences:
            for experience in experiences:
                try:
                    if isinstance(experience, str):
                        if ResumeTools.get_experience_from(experience) is None:
                            return generate_error_response(f"Experience in index {experiences.index(experience)} could not be found")

                        is_experiences_pk = True
                        if is_experiences_dict:
                            is_experiences_both = True

                        continue

                    if isinstance(experience, dict):
                        success, dict_or_error = ResumeTools.get_experience_data(None, False, experience)
                        if not success:
                            return generate_error_response(dict_or_error)  # type: ignore

                        is_experiences_dict = True
                        if is_experiences_pk:
                            is_experiences_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"Experiences list is invalid: {e}")

                return generate_error_response("Experiences list should contain strings (pk) or experiences dict (json)")

        # Competencies validations
        if competencies and not isinstance(competencies, list):
            return generate_error_response("Competencies should be an array")

        is_competencies_dict = False
        is_competencies_pk = False
        is_competencies_both = False
        if competencies:
            for competence in competencies:
                try:
                    if isinstance(competence, str):
                        if ResumeTools.get_competence_from(competence) is None:
                            return generate_error_response(f"Competence in index {competencies.index(competence)} could not be found")

                        is_competencies_pk = True
                        if is_competencies_dict:
                            is_competencies_both = True

                        continue
                    if isinstance(competence, dict):
                        success, dict_or_error = ResumeTools.get_competence_data(None, False, competence)
                        if not success:
                            return generate_error_response(dict_or_error)  # type: ignore

                        is_competencies_dict = True
                        if is_competencies_pk:
                            is_competencies_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"Competencies list is invalid: {e}")

                return generate_error_response("Competencies list should contain string (pk) or competencies dict (json)")

        # Courses validations
        if courses and not isinstance(courses, list):
            return generate_error_response("Courses shold be an array")

        is_courses_dict = False
        is_courses_pk = False
        is_courses_both = False
        if courses:
            for course in courses:
                try:
                    if isinstance(course, str):
                        if ResumeTools.get_course_from(course) is None:
                            return generate_error_response(f"Course in index {courses.index(course)} could not be found")

                        is_courses_pk = True
                        if is_courses_dict:
                            is_courses_both = True

                        continue
                    if isinstance(course, dict):
                        success, dict_or_error = ResumeTools.get_course_data(None, False, course)
                        if not success:
                            return generate_error_response(dict_or_error)  # type: ignore

                        is_courses_dict = True
                        if is_courses_pk:
                            is_courses_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"Courses list is invalid: {e}")

                return generate_error_response("Courses list should contain string (pk) or courses dict (json)")

        # References validations

        # Graduations validations

        # Projects validations

        # Links validations

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "experiences": {
                "is_dict": is_experiences_dict,
                "is_pk": is_experiences_pk,
                "is_both": is_experiences_both,
                "value": experiences
            },
            "competencies": {
                "is_dict": is_competencies_dict,
                "is_pk": is_competencies_pk,
                "is_both": is_competencies_both,
                "value": competencies
            },
            "courses": {
                "is_dict": is_courses_dict,
                "is_pk": is_courses_pk,
                "is_both": is_courses_both,
                "value": courses
            }
        }

        return (True, data)

    @staticmethod
    def get_experience_data(request, bypass_required: bool, json: dict | None = None) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        if json is not None:
            # required
            profile_pk = json.get("profile_pk", None)  # type: ignore

            # optional
            title = json.get("title", None)  # type: ignore
            description = json.get("description", None)  # type: ignore
            experience_company = json.get("experience_company", None)  # type: ignore
            experience_role = json.get("experience_role", None)  # type: ignore
            experience_description = json.get("experience_description", None)  # type: ignore
            experience_start_time = json.get("experience_start_time", None)  # type: ignore
            experience_end_time = json.get("experience_end_time", None)  # type: ignore
        else:
            # required
            profile_pk = request.data.get("profile_pk", None)  # type: ignore

            # optional
            title = request.data.get("title", None)  # type: ignore
            description = request.data.get("description", None)  # type: ignore
            experience_company = request.data.get("experience_company", None)  # type: ignore
            experience_role = request.data.get("experience_role", None)  # type: ignore
            experience_description = request.data.get("experience_description", None)  # type: ignore
            experience_start_time = request.data.get("experience_start_time", None)  # type: ignore
            experience_end_time = request.data.get("experience_end_time", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Experience company validations
        if experience_company and not isinstance(experience_company, str):
            return generate_error_response("Experience company should be a string")

        if experience_company and len(experience_company) > 255:
            return generate_error_response("Experience company should have a max length of 255 characters")

        # Experience role validations
        if experience_role and not isinstance(experience_role, str):
            return generate_error_response("Experience role should be a string")

        if experience_role and len(experience_role) > 255:
            return generate_error_response("Experience role should have a max length of 255 characters")

        # Experience description validation
        if experience_description and not isinstance(experience_description, str):
            return generate_error_response("Experience description should be a string")

        # Experience start time validations
        if experience_start_time and not isinstance(experience_start_time, str):
            return generate_error_response("Experience start time shold be a string")

        if experience_start_time and not ResumeTools.validate_date(experience_start_time):
            return generate_error_response("Experience start time should have an ISO date format")

        # Experience end time validations
        if experience_end_time and not isinstance(experience_end_time, str):
            return generate_error_response("Experience end time should be a string")

        if experience_end_time and not ResumeTools.validate_date(experience_end_time):
            return generate_error_response("Experience end time should have an ISO date format")

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "experience_company": experience_company,
            "experience_role": experience_role,
            "experience_description": experience_description,
            "experience_start_time": experience_start_time,
            "experience_end_time": experience_end_time
        }

        return (True, data)

    @staticmethod
    def get_competence_data(request, bypass_required: bool, json: dict | None = None) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        if json is not None:
            # required
            profile_pk = json.get("profile_pk", None)  # type: ignore

            # optional
            title = json.get("title", None)  # type: ignore
            description = json.get("description", None)  # type: ignore
            competence_name = json.get("competence_name", None)  # type: ignore
            competence_level = json.get("competence_level", None)  # type: ignore
        else:
            # required
            profile_pk = request.data.get("profile_pk", None)  # type: ignore

            # optional
            title = request.data.get("title", None)  # type: ignore
            description = request.data.get("description", None)  # type: ignore
            competence_name = request.data.get("competence_name", None)  # type: ignore
            competence_level = request.data.get("competence_level", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Competence name validation
        if competence_name and not isinstance(competence_name, str):
            return generate_error_response("Competence name should be a string")

        if competence_name and len(competence_name) > 255:
            return generate_error_response("Competence name should have a max length of 255 characters")

        # Competence level validation
        if competence_level and not isinstance(competence_level, str):
            return generate_error_response("Competence level should be a string")

        if competence_level and len(competence_level) > 255:
            return generate_error_response("Competence level should have a max length of 255 characters")

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "competence_name": competence_name,
            "competence_level": competence_level
        }

        return (True, data)

    @staticmethod
    def get_course_data(request, bypass_required: bool, json: dict | None = None) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        if json is not None:
            # required
            profile_pk = json.get("profile_pk", None)  # type: ignore

            # optional
            title = json.get("title", None)  # type: ignore
            description = json.get("description", None)  # type: ignore
            course_name = json.get("course_name", None)  # type: ignore
            course_locale = json.get("course_locale", None)  # type: ignore
            course_provider = json.get("course_provider", None)  # type: ignore
            course_hours = json.get("course_hours", None)  # type: ignore
            course_start_time = json.get("course_start_time", None)  # type: ignore
            course_end_time = json.get("course_end_time", None)  # type: ignore
        else:
            # required
            profile_pk = request.data.get("profile_pk", None)  # type: ignore

            # optional
            title = request.data.get("title", None)  # type: ignore
            description = request.data.get("description", None)  # type: ignore
            course_name = request.data.get("course_name", None)  # type: ignore
            course_locale = request.data.get("course_locale", None)  # type: ignore
            course_provider = request.data.get("course_provider", None)  # type: ignore
            course_hours = request.data.get("course_hours", None)  # type: ignore
            course_start_time = request.data.get("course_start_time", None)  # type: ignore
            course_end_time = request.data.get("course_end_time", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Course name validations
        if course_name and not isinstance(course_name, str):
            return generate_error_response("Course name should be a string")

        if course_name and len(course_name) > 255:
            return generate_error_response("Course name should have a max length of 255 characters")

        # Course locale validations
        if course_locale and not isinstance(course_locale, str):
            return generate_error_response("Course locale should be a string")

        if course_locale and len(course_locale) > 255:
            return generate_error_response("Course locale should have a max length of 255 characters")

        # Course provider validations
        if course_provider and not isinstance(course_provider, str):
            return generate_error_response("Course provider should be a string")

        if course_provider and len(course_provider) > 255:
            return generate_error_response("Course provider should have a max length of 255 characters")

        # Course hours validations
        if course_hours and not isinstance(course_hours, str):
            return generate_error_response("Course hours should be a string")

        if course_hours and len(course_hours) > 255:
            return generate_error_response("Course hours should have a max length of 255 characters")

        # Course start time validations
        if course_start_time and not isinstance(course_start_time, str):
            return generate_error_response("Course start time should be a string")

        if course_start_time and not ResumeTools.validate_date(course_start_time):
            return generate_error_response("Course start time should have an ISO date format")

        # Course end time validations
        if course_end_time and not isinstance(course_end_time, str):
            return generate_error_response("Course end time should be a string")

        if course_end_time and not ResumeTools.validate_date(course_end_time):
            return generate_error_response("Course end time should have an ISO date format")

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "course_name": course_name,
            "course_locale": course_locale,
            "course_provider": course_provider,
            "course_hours": course_hours,
            "course_start_time": course_start_time,
            "course_end_time": course_end_time
        }

        return (True, data)

    @staticmethod
    def get_reference_data(request, bypass_required: bool, json: dict | None = None) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        if json is not None:
            # required
            profile_pk = json.get("profile_pk", None)  # type: ignore

            # optional
            title = json.get("title", None)  # type: ignore
            description = json.get("description", None)  # type: ignore
            reference_name = json.get("reference_name", None)  # type: ignore
            reference_role = json.get("reference_role", None)  # type: ignore
            reference_company = json.get("reference_company", None)  # type: ignore
            reference_phone = json.get("reference_phone", None)  # type: ignore
            reference_email = json.get("reference_email", None)  # type: ignore
        else:
            # required
            profile_pk = request.data.get("profile_pk", None)  # type: ignore

            # optional
            title = request.data.get("title", None)  # type: ignore
            description = request.data.get("description", None)  # type: ignore
            reference_name = request.data.get("reference_name", None)  # type: ignore
            reference_role = request.data.get("reference_role", None)  # type: ignore
            reference_company = request.data.get("reference_company", None)  # type: ignore
            reference_phone = request.data.get("reference_phone", None)  # type: ignore
            reference_email = request.data.get("reference_email", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Reference name validations
        if reference_name and not isinstance(reference_name, str):
            return generate_error_response("Reference name should be a string")

        if reference_name and len(reference_name) > 255:
            return generate_error_response("Reference name should have a max length of 255 characters")

        # Reference role validations
        if reference_role and not isinstance(reference_role, str):
            return generate_error_response("Reference role should be a string")

        if reference_role and len(reference_role) > 255:
            return generate_error_response("Reference role should have a max length of 255 characters")

        # Reference company validations
        if reference_company and not isinstance(reference_company, str):
            return generate_error_response("Reference company should be a string")

        if reference_company and len(reference_company) > 255:
            return generate_error_response("Reference company should have a max length of 255 characters")

        # Reference phone validations
        if reference_phone and not isinstance(reference_phone, str):
            return generate_error_response("Reference phone should be a string")

        if reference_phone and len(reference_phone) > 255:
            return generate_error_response("Reference phone should have a max length of 255 characters")

        # Reference email validations
        if reference_email and not isinstance(reference_email, str):
            return generate_error_response("Reference email should be a string")

        if reference_email and len(reference_email) > 255:
            return generate_error_response("Reference email should have a max length of 255 characters")

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "reference_name": reference_name,
            "reference_role": reference_role,
            "reference_company": reference_company,
            "reference_phone": reference_phone,
            "reference_email": reference_email
        }

        return (True, data)

    @staticmethod
    def get_graduation_data(request, bypass_required: bool, json: dict | None = None) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        if json is not None:
            # required
            profile_pk = json.get("profile_pk", None)  # type: ignore

            # optional
            title = json.get("title", None)  # type: ignore
            description = json.get("description", None)  # type: ignore
            graduation_type = json.get("graduation_type", None)  # type: ignore
            graduation_period = json.get("graduation_period", None)  # type: ignore
            graduation_start_time = json.get("graduation_start_time", None)  # type: ignore
            graduation_end_time = json.get("graduation_end_time", None)  # type: ignore
        else:
            # required
            profile_pk = request.data.get("profile_pk", None)  # type: ignore

            # optional
            title = request.data.get("title", None)  # type: ignore
            description = request.data.get("description", None)  # type: ignore
            graduation_type = request.data.get("graduation_type", None)  # type: ignore
            graduation_period = request.data.get("graduation_period", None)  # type: ignore
            graduation_start_time = request.data.get("graduation_start_time", None)  # type: ignore
            graduation_end_time = request.data.get("graduation_end_time", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Type validations
        if graduation_type and not isinstance(graduation_type, str):
            return generate_error_response("Graduation type should be a string")

        if graduation_type and len(graduation_type) > 150:
            return generate_error_response("Graduation type should have a max length of 150 characters")

        # Period validations
        if graduation_period and not isinstance(graduation_period, str):
            return generate_error_response("Graduation period should be a string")

        if graduation_period and len(graduation_period) > 150:
            return generate_error_response("Graduation period should have a max length of 150 characters")

        # Start time validations
        if graduation_start_time and not isinstance(graduation_start_time, str):
            return generate_error_response("Graduation start time should be a string")

        if graduation_start_time and not ResumeTools.validate_date(graduation_start_time):
            return generate_error_response("Graduation start time should have a ISO date format")

        # End time validations
        if graduation_end_time and not isinstance(graduation_end_time, str):
            return generate_error_response("Graduation end time should be a string")

        if graduation_end_time and not ResumeTools.validate_date(graduation_end_time):
            return generate_error_response("Graduation end time should have a ISO date format")

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "graduation_type": graduation_type,
            "graduation_period": graduation_period,
            "graduation_start_time": graduation_start_time,
            "graduation_end_time": graduation_end_time
        }

        return (True, data)

    @staticmethod
    def get_project_data(request, bypass_required: bool, json: dict | None = None) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        if json is not None:
            # required
            profile_pk = json.get("profile_pk", None)  # type: ignore

            # optional
            title = json.get("title", None)  # type: ignore
            description = json.get("description", None)  # type: ignore
            project_name = json.get("project_name", None)  # type: ignore
            project_description = json.get("project_description", None)  # type: ignore
            project_link = json.get("project_link", None)  # type: ignore
        else:
            # required
            profile_pk = request.data.get("profile_pk", None)  # type: ignore

            # optional
            title = request.data.get("title", None)  # type: ignore
            description = request.data.get("description", None)  # type: ignore
            project_name = request.data.get("project_name", None)  # type: ignore
            project_description = request.data.get("project_description", None)  # type: ignore
            project_link = request.data.get("project_link", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        # Project name validations
        if project_name and not isinstance(project_name, str):
            return generate_error_response("Project name should be a string")

        if project_name and len(project_name) > 255:
            return generate_error_response("Project name should have a max length of 255 characters")

        # Project description validations
        if project_description and not isinstance(project_description, str):
            return generate_error_response("Project description should be a string")

        # Project link validation
        if project_link and not isinstance(project_link, str):
            return generate_error_response("Project link should be a string")

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "project_name": project_name,
            "project_description": project_description,
            "project_link": project_link
        }

        return (True, data)

    @staticmethod
    def get_link_data(request, bypass_required: bool, json: dict | None = None) -> tuple[bool, dict[str, Any | None] | str]:
        def generate_error_response(text: str):
            return (False, text)

        if json is not None:
            # required
            profile_pk = json.get("profile_pk", None)  # type: ignore
            url = json.get("url", None)  # type: ignore

            # optional
            title = json.get("title", None)  # type: ignore
            description = json.get("description", None)  # type: ignore
        else:
            # required
            profile_pk = request.data.get("profile_pk", None)  # type: ignore
            url = request.data.get("url", None)  # type: ignore

            # optional
            title = request.data.get("title", None)  # type: ignore
            description = request.data.get("description", None)  # type: ignore

        # Profile PK validation
        if profile_pk is None and not bypass_required:
            return generate_error_response("Profile PK is required")

        if profile_pk and not isinstance(profile_pk, str):
            return generate_error_response("Profile PK should be a string")

        if profile_pk and not UserProfile.objects.filter(pk=profile_pk).first():
            return generate_error_response("Profile not found")

        # Url validation
        if url is None and not bypass_required:
            return generate_error_response("URL is required")

        if url and not isinstance(url, str):
            return generate_error_response("URL should be a string")

        # Title validations
        if title and not isinstance(title, str):
            return generate_error_response("Title should be a string")

        if title and len(title) > 255:
            return generate_error_response("Title should have a max length of 255 characters")

        # Description validations
        if description and not isinstance(description, str):
            return generate_error_response("Description should be a string")

        data = {
            "profile_pk": profile_pk,
            "title": title,
            "description": description,
            "url": url
        }

        return (True, data)

    # ====== Resume ====== #
    @staticmethod
    def get_resume_from(pk: str) -> models.ResumeModel | None:
        if pk:
            return models.ResumeModel.objects.filter(pk=pk).first()

        return None

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
    def get_experience_from(pk: str) -> models.ResumeExperience | None:
        if pk:
            return models.ResumeExperience.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_experience(request: HttpRequest) -> models.ResumeExperience | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeExperience.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_experiences(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeExperience.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeExperience.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeExperience.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_experience(request: HttpRequest) -> models.ResumeExperience:
        pass

    @staticmethod
    def edit_experience(request: HttpRequest, experience: models.ResumeExperience):
        pass

    @staticmethod
    def delete_experience(request: HttpRequest, experience: models.ResumeExperience):
        experience_model = ResumeTools.get_experience(request)

        if experience_model is None:
            return

        if experience_model.pk != experience.pk:
            return

        experience.delete()

    # ====== Competence ====== #
    @staticmethod
    def get_competence_from(pk: str) -> models.ResumeCompetence | None:
        if pk:
            return models.ResumeCompetence.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_competence(request: HttpRequest) -> models.ResumeCompetence | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeCompetence.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_competencies(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeCompetence.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeCompetence.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeCompetence.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_competence(request: HttpRequest) -> models.ResumeCompetence:
        pass

    @staticmethod
    def edit_competence(request: HttpRequest, competence: models.ResumeCompetence):
        pass

    @staticmethod
    def delete_competence(request: HttpRequest, competence: models.ResumeCompetence):
        competence_model = ResumeTools.get_competence(request)

        if competence_model is None:
            return

        if competence_model.pk != competence.pk:
            return

        competence.delete()

    # ====== Course ====== #
    @staticmethod
    def get_course_from(pk: str) -> models.ResumeCourse | None:
        if pk:
            return models.ResumeCourse.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_course(request: HttpRequest) -> models.ResumeCourse | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeCourse.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_courses(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeCourse.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeCourse.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeCourse.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_course(request: HttpRequest) -> models.ResumeCourse:
        pass

    @staticmethod
    def edit_course(request: HttpRequest, course: models.ResumeCourse):
        pass

    @staticmethod
    def delete_course(request: HttpRequest, course: models.ResumeCourse):
        course_model = ResumeTools.get_course(request)

        if course_model is None:
            return

        if course_model.pk != course.pk:
            return

        course.delete()

    # ====== Reference ====== #
    @staticmethod
    def get_reference_from(pk: str) -> models.ResumeReference | None:
        if pk:
            return models.ResumeReference.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_reference(request: HttpRequest) -> models.ResumeReference | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeReference.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_references(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeReference.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeReference.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeReference.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_reference(request: HttpRequest) -> models.ResumeReference:
        pass

    @staticmethod
    def edit_reference(request: HttpRequest, reference: models.ResumeReference):
        pass

    @staticmethod
    def delete_reference(request: HttpRequest, reference: models.ResumeReference):
        reference_model = ResumeTools.get_reference(request)

        if reference_model is None:
            return

        if reference_model.pk != reference.pk:
            return

        reference.delete()

    # ====== Graduation ====== #
    @staticmethod
    def get_graduation_from(pk: str) -> models.ResumeGraduation | None:
        if pk:
            return models.ResumeGraduation.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_graduation(request: HttpRequest) -> models.ResumeGraduation | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeGraduation.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_graduations(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeGraduation.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeGraduation.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeGraduation.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_graduation(request: HttpRequest) -> models.ResumeGraduation:
        pass

    @staticmethod
    def edit_graduation(request: HttpRequest, graduation: models.ResumeGraduation):
        pass

    @staticmethod
    def delete_graduation(request: HttpRequest, graduation: models.ResumeGraduation):
        graduation_model = ResumeTools.get_graduation(request)

        if graduation_model is None:
            return

        if graduation_model.pk != graduation.pk:
            return

        graduation.delete()

    # ====== Project ====== #
    @staticmethod
    def get_project_from(pk: str) -> models.ResumeProject | None:
        if pk:
            return models.ResumeProject.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_project(request: HttpRequest) -> models.ResumeProject | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeProject.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_projects(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeProject.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeProject.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeProject.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_project(request: HttpRequest) -> models.ResumeProject:
        pass

    @staticmethod
    def edit_project(request: HttpRequest, project: models.ResumeProject):
        pass

    @staticmethod
    def delete_project(request: HttpRequest, project: models.ResumeProject):
        project_model = ResumeTools.get_project(request)

        if project_model is None:
            return

        if project_model.pk != project.pk:
            return

        project.delete()

    # ====== Link ====== #
    @staticmethod
    def get_link_from(pk: str) -> models.ResumeLink | None:
        if pk:
            return models.ResumeLink.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_link(request: HttpRequest) -> models.ResumeLink | None:
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            return models.ResumeLink.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_all_links(request: HttpRequest) -> Any | None:
        user_pk = request.query_params.get("user_pk", None)  # type: ignore

        if user_pk:
            return models.ResumeLink.objects.filter(profile__user__pk=user_pk)

        profile_pk = request.query_params.get("profile_pk", None)  # type: ignore

        if profile_pk:
            return models.ResumeLink.objects.filter(profile__pk=profile_pk)

        slug = request.query_params.get("slug", None)  # type: ignore

        if slug:
            return models.ResumeLink.objects.filter(profile__slug=slug)

        return None

    @staticmethod
    def create_link(request: HttpRequest) -> models.ResumeLink:
        pass

    @staticmethod
    def edit_link(request: HttpRequest, link: models.ResumeLink):
        pass

    @staticmethod
    def delete_link(request: HttpRequest, link: models.ResumeLink):
        link_model = ResumeTools.get_link(request)

        if link_model is None:
            return

        if link_model.pk != link.pk:
            return

        link.delete()


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
                        schema=coreschema.Array(coreschema.Object()),
                        description="Experiences dict or PK array"
                    ),
                    coreapi.Field(
                        name="competencies",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Competencies dict or PK array"
                    ),
                    coreapi.Field(
                        name="courses",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Courses dict or PK array"
                    ),
                    coreapi.Field(
                        name="references",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="References dict or PK array"
                    ),
                    coreapi.Field(
                        name="graduations",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Graduations dict or PK array"
                    ),
                    coreapi.Field(
                        name="projects",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Projects dict or PK array"
                    ),
                    coreapi.Field(
                        name="links",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Links dict or PK array"
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
                        schema=coreschema.Array(coreschema.Object()),
                        description="Experiences dict or PK array"
                    ),
                    coreapi.Field(
                        name="competencies",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Competencies dict or PK array"
                    ),
                    coreapi.Field(
                        name="courses",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Courses dict or PK array"
                    ),
                    coreapi.Field(
                        name="references",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="References dict or PK array"
                    ),
                    coreapi.Field(
                        name="graduations",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Graduations dict or PK array"
                    ),
                    coreapi.Field(
                        name="projects",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Projects dict or PK array"
                    ),
                    coreapi.Field(
                        name="links",
                        location='form',
                        required=False,
                        schema=coreschema.Array(coreschema.Object()),
                        description="Links dict or PK array"
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
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            experience_model: models.ResumeExperience | None = ResumeTools.get_experience(request)

            if experience_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_experience_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Experience found")

            serializer = serializers.ExperienceSerializer(experience_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        experience_models: Any | None = ResumeTools.get_all_experiences(request)

        if experience_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_experience_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Experiences found")

        serializer = serializers.ExperienceSerializer(experience_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        experience_model = ResumeTools.get_experience(request)

        if experience_model is not None:
            ResumeTools.delete_experience(request, experience_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_experience_str)


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
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            competence_model: models.ResumeCompetence | None = ResumeTools.get_competence(request)

            if competence_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_competence_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Competence found")

            serializer = serializers.CompetenceSerializer(competence_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        competence_models: Any | None = ResumeTools.get_all_competencies(request)

        if competence_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_competence_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "competencies found")

        serializer = serializers.CompetenceSerializer(competence_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        competence_model = ResumeTools.get_competence(request)

        if competence_model is not None:
            ResumeTools.delete_competence(request, competence_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_competence_str)


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
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            course_model: models.ResumeCourse | None = ResumeTools.get_course(request)

            if course_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_course_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Course found")

            serializer = serializers.CourseSerializer(course_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        course_models: Any | None = ResumeTools.get_all_courses(request)

        if course_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_course_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Courses found")

        serializer = serializers.CourseSerializer(course_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        course_model = ResumeTools.get_course(request)

        if course_model is not None:
            ResumeTools.delete_course(request, course_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_course_str)


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
                        name="reference_email",
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
                        name="reference_email",
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
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            reference_model: models.ResumeReference | None = ResumeTools.get_reference(request)

            if reference_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_reference_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Reference found")

            serializer = serializers.ReferenceSerializer(reference_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        reference_models: Any | None = ResumeTools.get_all_references(request)

        if reference_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_reference_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "References found")

        serializer = serializers.ReferenceSerializer(reference_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        reference_model = ResumeTools.get_reference(request)

        if reference_model is not None:
            ResumeTools.delete_reference(request, reference_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_reference_str)


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
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            graduation_model: models.ResumeGraduation | None = ResumeTools.get_graduation(request)

            if graduation_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_graduation_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Graduation found")

            serializer = serializers.GraduationSerializer(graduation_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        graduation_models: Any | None = ResumeTools.get_all_graduations(request)

        if graduation_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_graduation_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Graduations found")

        serializer = serializers.GraduationSerializer(graduation_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        graduation_model = ResumeTools.get_graduation(request)

        if graduation_model is not None:
            ResumeTools.delete_graduation(request, graduation_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_graduation_str)


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
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            project_model: models.ResumeProject | None = ResumeTools.get_project(request)

            if project_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_project_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Project found")

            serializer = serializers.ProjectSerializer(project_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        project_models: Any | None = ResumeTools.get_all_projects(request)

        if project_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_project_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Projects found")

        serializer = serializers.ProjectSerializer(project_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        project_model = ResumeTools.get_project(request)

        if project_model is not None:
            ResumeTools.delete_project(request, project_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_project_str)


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
        pk = request.query_params.get("pk", None)  # type: ignore

        if pk:
            link_model: models.ResumeLink | None = ResumeTools.get_link(request)

            if link_model is None:
                return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                    self.not_found_link_str)

            response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                              "Link found")

            serializer = serializers.LinkSerializer(link_model, many=False)
            response_data['content'] = serializer.data
            return Response(data=response_data, status=status.HTTP_200_OK)

        link_models: Any | None = ResumeTools.get_all_links(request)

        if link_models is None:
            return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                                self.not_found_link_str)

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Links found")

        serializer = serializers.LinkSerializer(link_models, many=True)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        link_model = ResumeTools.get_link(request)

        if link_model is not None:
            ResumeTools.delete_link(request, link_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_link_str)
