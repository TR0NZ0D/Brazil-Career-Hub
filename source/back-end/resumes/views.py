import coreapi
import coreschema

from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

from api.tools.api_tools import description_generator
from api.views import Base
from . import serializers
from . import models
from users.models import UserProfile
from typing import Any
from datetime import datetime
from datetime import date as datetime_date


# ========== Generics ========== #
class ResumeTools:
    # ====== Generic Validations ====== #
    @staticmethod
    def validate_date(date: str) -> bool:
        if date and not isinstance(date, str):
            return False

        if date:
            try:
                formatted_date = datetime_date.fromisoformat(date)
                return formatted_date.isoformat() == date
            except ValueError:
                return False

        return False

    # ====== Generics ====== #
    @staticmethod
    def convert_time(date: str) -> datetime_date | None:
        if date and not isinstance(date, str):
            return None

        if date:
            try:
                formatted_date = datetime_date.fromisoformat(date)
                return formatted_date
            except ValueError:
                return None

        return None

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
                            return generate_error_response(f"Experience PK {experience} in index {experiences.index(experience)} could not be found")

                        is_experiences_pk = True
                        if is_experiences_dict:
                            is_experiences_both = True

                        continue

                    if isinstance(experience, dict):
                        success, dict_or_error = ResumeTools.get_experience_data(None, False, experience)
                        if not success:
                            return generate_error_response(f"Experience dict in index {experiences.index(experience)} is invalid: {dict_or_error}")

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
                            return generate_error_response(f"Competence PK {competence} in index {competencies.index(competence)} could not be found")

                        is_competencies_pk = True
                        if is_competencies_dict:
                            is_competencies_both = True

                        continue
                    if isinstance(competence, dict):
                        success, dict_or_error = ResumeTools.get_competence_data(None, False, competence)
                        if not success:
                            return generate_error_response(f"Competence dict in index {competencies.index(competence)} is invalid: {dict_or_error}")

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
                            return generate_error_response(f"Course PK {course} in index {courses.index(course)} could not be found")

                        is_courses_pk = True
                        if is_courses_dict:
                            is_courses_both = True

                        continue
                    if isinstance(course, dict):
                        success, dict_or_error = ResumeTools.get_course_data(None, False, course)
                        if not success:
                            return generate_error_response(f"Course dict in index {courses.index(course)} is invalid: {dict_or_error}")

                        is_courses_dict = True
                        if is_courses_pk:
                            is_courses_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"Courses list is invalid: {e}")

                return generate_error_response("Courses list should contain string (pk) or courses dict (json)")

        # References validations
        if references and not isinstance(references, list):
            return generate_error_response("References should be an array")

        is_references_pk = False
        is_references_dict = False
        is_references_both = False
        if references:
            for reference in references:
                try:
                    if isinstance(reference, str):
                        if ResumeTools.get_reference_from(reference) is None:
                            return generate_error_response(f"Reference PK {reference} in index {references.index(reference)} could not be found")

                        is_references_pk = True
                        if is_references_dict:
                            is_references_both = True

                        continue

                    if isinstance(reference, dict):
                        success, dict_or_error = ResumeTools.get_reference_data(None, False, reference)
                        if not success:
                            return generate_error_response(f"Reference dict in index {references.index(reference)} is invalid: {dict_or_error}")

                        is_references_dict = True
                        if is_references_pk:
                            is_references_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"References list is invalid: {e}")

                return generate_error_response("References list should contain strings (pk) or references dict (json)")

        # Graduations validations
        if graduations and not isinstance(graduations, list):
            return generate_error_response("Graduations should be an array")

        is_graduations_pk = False
        is_graduations_dict = False
        is_graduations_both = False
        if graduations:
            for graduation in graduations:
                try:
                    if isinstance(graduation, str):
                        if ResumeTools.get_reference_from(graduation) is None:
                            return generate_error_response(f"Graduation PK {graduation} in index {graduations.index(graduation)} could not be found")

                        is_graduations_pk = True
                        if is_graduations_dict:
                            is_graduations_both = True

                        continue

                    if isinstance(graduation, dict):
                        success, dict_or_error = ResumeTools.get_graduation_data(None, False, graduation)
                        if not success:
                            return generate_error_response(f"Graduation dict in index {graduations.index(graduation)} is invalid: {dict_or_error}")

                        is_graduations_dict = True
                        if is_graduations_pk:
                            is_graduations_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"Graduations list is invalid: {e}")

                return generate_error_response("Graduations list should contain strings (pk) or graduations dict (json)")

        # Projects validations
        if projects and not isinstance(projects, list):
            return generate_error_response("Projects should be an array")

        is_projects_pk = False
        is_projects_dict = False
        is_projects_both = False
        if projects:
            for project in projects:
                try:
                    if isinstance(project, str):
                        if ResumeTools.get_project_from(project) is None:
                            return generate_error_response(f"Project PK {project} in index {projects.index(project)} could not be found")

                        is_projects_pk = True
                        if is_projects_dict:
                            is_projects_both = True

                        continue

                    if isinstance(project, dict):
                        success, dict_or_error = ResumeTools.get_project_data(None, False, project)
                        if not success:
                            return generate_error_response(f"Project dict in index {projects.index(project)} is invalid: {dict_or_error}")

                        is_projects_dict = True
                        if is_projects_pk:
                            is_projects_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"Projects list is invalid: {e}")

                return generate_error_response("Projects list should contain strings (pk) or graduations dict (json)")

        # Links validations
        if links and not isinstance(links, list):
            return generate_error_response("Links should be an array")

        is_links_pk = False
        is_links_dict = False
        is_links_both = False
        if links:
            for link in links:
                try:
                    if isinstance(link, str):
                        if ResumeTools.get_link_from(link) is None:
                            return generate_error_response(f"Link PK {link} in index {links.index(link)} could not be found")

                        is_links_pk = True
                        if is_links_dict:
                            is_links_both = True

                        continue
                    if isinstance(link, dict):
                        success, dict_or_error = ResumeTools.get_link_data(None, False, link)
                        if not success:
                            return generate_error_response(f"Link dict in index {links.index(link)} is invalid: {dict_or_error}")

                        is_links_dict = True
                        if is_links_pk:
                            is_links_both = True

                        continue
                except Exception as e:
                    return generate_error_response(f"Links list is invalid: {e}")

                return generate_error_response("Links list should contain strings (pk) or links dict (json)")

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
            },
            "references": {
                "is_dict": is_references_dict,
                "is_pk": is_references_pk,
                "is_both": is_references_both,
                "value": references
            },
            "graduations": {
                "is_dict": is_graduations_dict,
                "is_pk": is_graduations_pk,
                "is_both": is_graduations_both,
                "value": graduations
            },
            "projects": {
                "is_dict": is_projects_dict,
                "is_pk": is_projects_pk,
                "is_both": is_projects_both,
                "value": projects
            },
            "links": {
                "is_dict": is_links_dict,
                "is_pk": is_links_pk,
                "is_both": is_links_both,
                "value": links
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
            return generate_error_response("Experience start time should have an ISO date format (yyyy-MM-dd)")

        # Experience end time validations
        if experience_end_time and not isinstance(experience_end_time, str):
            return generate_error_response("Experience end time should be a string")

        if experience_end_time and not ResumeTools.validate_date(experience_end_time):
            return generate_error_response("Experience end time should have an ISO date format (yyyy-MM-dd)")

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
            return generate_error_response("Course start time should have an ISO date format (yyyy-MM-dd)")

        # Course end time validations
        if course_end_time and not isinstance(course_end_time, str):
            return generate_error_response("Course end time should be a string")

        if course_end_time and not ResumeTools.validate_date(course_end_time):
            return generate_error_response("Course end time should have an ISO date format (yyyy-MM-dd)")

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
    def create_resume(request: HttpRequest) -> tuple[bool, models.ResumeModel | str]:
        success, data_or_error = ResumeTools.get_resume_data(request, False)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore

        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        experiences_dict: dict | None = data.get("experiences", None)
        competencies_dict: dict | None = data.get("competencies", None)
        courses_dict: dict | None = data.get("courses", None)
        references_dict: dict | None = data.get("references", None)
        graduations_dict: dict | None = data.get("graduations", None)
        projects_dict: dict | None = data.get("projects", None)
        links_dict: dict | None = data.get("links", None)

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if profile is None:
            return (False, "Profile not found")

        resume = models.ResumeModel.objects.create(profile=profile,
                                                   title=title,
                                                   description=description)

        # Experiences
        if experiences_dict is not None:
            experiences = experiences_dict.get("value", None)

            if experiences is not None and isinstance(experiences, list):
                for experience in experiences:
                    exp_obj = ResumeTools.get_experience_obj(request, experience)
                    if exp_obj is None:
                        continue

                    success, obj_or_error = exp_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeExperience):
                        continue

                    success, model_or_error = ResumeTools.add_experience_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Competencies
        if competencies_dict is not None:
            competencies = competencies_dict.get("value", None)

            if competencies is not None and isinstance(competencies, list):
                for competence in competencies:
                    competence_obj = ResumeTools.get_competence_obj(request, competence)
                    if competence_obj is None:
                        continue

                    success, obj_or_error = competence_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeCompetence):
                        continue

                    success, model_or_error = ResumeTools.add_competence_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Courses
        if courses_dict is not None:
            courses = courses_dict.get("value", None)

            if courses is not None and isinstance(courses, list):
                for course in courses:
                    course_obj = ResumeTools.get_course_obj(request, course)
                    if course_obj is None:
                        continue

                    success, obj_or_error = course_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeCourse):
                        continue

                    success, model_or_error = ResumeTools.add_course_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # References
        if references_dict is not None:
            references = references_dict.get("value", None)

            if references is not None and isinstance(references, list):
                for reference in references:
                    reference_obj = ResumeTools.get_reference_obj(request, reference)
                    if reference_obj is None:
                        continue

                    success, obj_or_error = reference_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeReference):
                        continue

                    success, model_or_error = ResumeTools.add_reference_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Graduations
        if graduations_dict is not None:
            graduations = graduations_dict.get("value", None)

            if graduations is not None and isinstance(graduations, list):
                for graduation in graduations:
                    graduation_obj = ResumeTools.get_graduation_obj(request, graduation)
                    if graduation_obj is None:
                        continue

                    success, obj_or_error = graduation_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeGraduation):
                        continue

                    success, model_or_error = ResumeTools.add_graduation_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Projects
        if projects_dict is not None:
            projects = projects_dict.get("value", None)

            if projects is not None and isinstance(projects, list):
                for project in projects:
                    project_obj = ResumeTools.get_project_obj(request, project)
                    if project_obj is None:
                        continue

                    success, obj_or_error = project_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeProject):
                        continue

                    success, model_or_error = ResumeTools.add_project_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Links
        if links_dict is not None:
            links = links_dict.get("value", None)

            if links is not None and isinstance(links, list):
                for link in links:
                    link_obj = ResumeTools.get_link_obj(request, link)
                    if link_obj is None:
                        continue

                    success, obj_or_error = link_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeLink):
                        continue

                    success, model_or_error = ResumeTools.add_link_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        resume.save()

        return (True, resume)

    @staticmethod
    def edit_resume(request: HttpRequest, resume: models.ResumeModel) -> tuple[bool, str | models.ResumeModel]:
        success, data_or_error = ResumeTools.get_resume_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore

        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        experiences_dict: dict | None = data.get("experiences", None)
        competencies_dict: dict | None = data.get("competencies", None)
        courses_dict: dict | None = data.get("courses", None)
        references_dict: dict | None = data.get("references", None)
        graduations_dict: dict | None = data.get("graduations", None)
        projects_dict: dict | None = data.get("projects", None)
        links_dict: dict | None = data.get("links", None)

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            resume.profile = profile

        if title is not None:
            resume.title = title

        if description is not None:
            resume.description = description

        # Experiences
        if experiences_dict is not None:
            resume.experiences.clear()
            resume.save()

            experiences = experiences_dict.get("value", None)

            if experiences is not None and isinstance(experiences, list):
                for experience in experiences:
                    exp_obj = ResumeTools.get_experience_obj(request, experience)
                    if exp_obj is None:
                        continue

                    success, obj_or_error = exp_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeExperience):
                        continue

                    success, model_or_error = ResumeTools.add_experience_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Competencies
        if competencies_dict is not None:
            resume.competencies.clear()
            resume.save()

            competencies = competencies_dict.get("value", None)

            if competencies is not None and isinstance(competencies, list):
                for competence in competencies:
                    competence_obj = ResumeTools.get_competence_obj(request, competence)
                    if competence_obj is None:
                        continue

                    success, obj_or_error = competence_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeCompetence):
                        continue

                    success, model_or_error = ResumeTools.add_competence_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Courses
        if courses_dict is not None:
            resume.courses.clear()
            resume.save()

            courses = courses_dict.get("value", None)

            if courses is not None and isinstance(courses, list):
                for course in courses:
                    course_obj = ResumeTools.get_course_obj(request, course)
                    if course_obj is None:
                        continue

                    success, obj_or_error = course_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeCourse):
                        continue

                    success, model_or_error = ResumeTools.add_course_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # References
        if references_dict is not None:
            resume.references.clear()
            resume.save()

            references = references_dict.get("value", None)

            if references is not None and isinstance(references, list):
                for reference in references:
                    reference_obj = ResumeTools.get_reference_obj(request, reference)
                    if reference_obj is None:
                        continue

                    success, obj_or_error = reference_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeReference):
                        continue

                    success, model_or_error = ResumeTools.add_reference_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Graduations
        if graduations_dict is not None:
            resume.graduations.clear()
            resume.save()

            graduations = graduations_dict.get("value", None)

            if graduations is not None and isinstance(graduations, list):
                for graduation in graduations:
                    graduation_obj = ResumeTools.get_graduation_obj(request, graduation)
                    if graduation_obj is None:
                        continue

                    success, obj_or_error = graduation_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeGraduation):
                        continue

                    success, model_or_error = ResumeTools.add_graduation_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Projects
        if projects_dict is not None:
            resume.projects.clear()
            resume.save()

            projects = projects_dict.get("value", None)

            if projects is not None and isinstance(projects, list):
                for project in projects:
                    project_obj = ResumeTools.get_project_obj(request, project)
                    if project_obj is None:
                        continue

                    success, obj_or_error = project_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeProject):
                        continue

                    success, model_or_error = ResumeTools.add_project_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        # Links
        if links_dict is not None:
            resume.links.clear()
            resume.save()

            links = links_dict.get("value", None)

            if links is not None and isinstance(links, list):
                for link in links:
                    link_obj = ResumeTools.get_link_obj(request, link)
                    if link_obj is None:
                        continue

                    success, obj_or_error = link_obj
                    if not success:
                        return (False, obj_or_error)  # type: ignore

                    if not isinstance(obj_or_error, models.ResumeLink):
                        continue

                    success, model_or_error = ResumeTools.add_link_to_resume(request, resume, obj_or_error)
                    if not success:
                        return (False, model_or_error)  # type: ignore

        resume.save()

        return (True, resume)

    @staticmethod
    def delete_resume(request: HttpRequest, resume: models.ResumeModel):
        resume_model = ResumeTools.get_resume(request)

        if resume_model is None:
            return

        if resume_model.pk != resume.pk:
            return

        resume.delete()

    @staticmethod
    def add_experience_to_resume(request: HttpRequest, resume: models.ResumeModel, experience: models.ResumeExperience) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.experiences.add(experience)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while adding experience to resume: {e}")

    @staticmethod
    def add_competence_to_resume(request: HttpRequest, resume: models.ResumeModel, competence: models.ResumeCompetence) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.competencies.add(competence)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while adding competence to resume: {e}")

    @staticmethod
    def add_course_to_resume(request: HttpRequest, resume: models.ResumeModel, course: models.ResumeCourse) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.courses.add(course)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while adding course to resume: {e}")

    @staticmethod
    def add_reference_to_resume(request: HttpRequest, resume: models.ResumeModel, reference: models.ResumeReference) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.references.add(reference)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while adding reference to resume: {e}")

    @staticmethod
    def add_graduation_to_resume(request: HttpRequest, resume: models.ResumeModel, graduation: models.ResumeGraduation) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.graduations.add(graduation)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while adding graduation to resume: {e}")

    @staticmethod
    def add_project_to_resume(request: HttpRequest, resume: models.ResumeModel, project: models.ResumeProject) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.projects.add(project)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while adding project to resume: {e}")

    @staticmethod
    def add_link_to_resume(request: HttpRequest, resume: models.ResumeModel, link: models.ResumeLink) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.links.add(link)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while adding link to resume: {e}")

    @staticmethod
    def remove_experience_from_resume(request: HttpRequest, resume: models.ResumeModel, experience: models.ResumeExperience) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.experiences.remove(experience)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while removing experience from resume: {e}")

    @staticmethod
    def remove_competence_from_resume(request: HttpRequest, resume: models.ResumeModel, competence: models.ResumeCompetence) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.competencies.remove(competence)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while removing competence from resume: {e}")

    @staticmethod
    def remove_course_from_resume(request: HttpRequest, resume: models.ResumeModel, course: models.ResumeCourse) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.courses.remove(course)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while removing course from resume: {e}")

    @staticmethod
    def remove_reference_from_resume(request: HttpRequest, resume: models.ResumeModel, reference: models.ResumeReference) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.references.remove(reference)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while removing reference from resume: {e}")

    @staticmethod
    def remove_graduation_from_resume(request: HttpRequest, resume: models.ResumeModel, graduation: models.ResumeGraduation) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.graduations.remove(graduation)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while removing graduation from resume: {e}")

    @staticmethod
    def remove_project_from_resume(request: HttpRequest, resume: models.ResumeModel, project: models.ResumeProject) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.projects.remove(project)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while removing project from resume: {e}")

    @staticmethod
    def remove_link_from_resume(request: HttpRequest, resume: models.ResumeModel, link: models.ResumeLink) -> tuple[bool, str | models.ResumeModel]:
        try:
            resume.links.remove(link)
            resume.save()
            return (True, resume)
        except Exception as e:
            return (False, f"Error while removing link from resume: {e}")

    # ====== Experience ====== #
    @staticmethod
    def get_experience_from(pk: str) -> models.ResumeExperience | None:
        if pk:
            return models.ResumeExperience.objects.filter(pk=pk).first()

        return None

    @staticmethod
    def get_experience_obj(request, source: dict | str | None = None) -> tuple[bool, models.ResumeExperience | str] | None:
        if isinstance(source, dict):
            success, exp_obj_or_error = ResumeTools.create_experience(request, source)
            if not success:
                return (False, exp_obj_or_error)  # type: ignore

            exp_obj: models.ResumeExperience = exp_obj_or_error  # type: ignore
            return (True, exp_obj)

        if isinstance(source, str):
            exp_obj = ResumeTools.get_experience_from(source)  # type: ignore
            if exp_obj is None:
                return (False, f"Experience ID #{source} not found")

            return (True, exp_obj)

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
    def create_experience(request: HttpRequest, json: dict | None = None) -> tuple[bool, models.ResumeExperience | str]:
        success, data_or_error = ResumeTools.get_experience_data(request, False, json)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        experience_company = data.get("experience_company", "")
        experience_role = data.get("experience_role", "")
        experience_description = data.get("experience_description", "")
        experience_start_time = ResumeTools.convert_time(data.get("experience_start_time", ""))
        experience_end_time = ResumeTools.convert_time(data.get("experience_end_time", ""))

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if not profile:
            return (False, "Profile not found")

        experience = models.ResumeExperience.objects.create(profile=profile,
                                                            title=title,
                                                            description=description,
                                                            experience_company=experience_company,
                                                            experience_role=experience_role,
                                                            experience_description=experience_description,
                                                            experience_start_time=experience_start_time,
                                                            experience_end_time=experience_end_time)

        return (True, experience)

    @staticmethod
    def edit_experience(request: HttpRequest, experience: models.ResumeExperience) -> tuple[bool, models.ResumeExperience | str]:
        success, data_or_error = ResumeTools.get_experience_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", None)
        title = data.get("title", None)
        description = data.get("description", None)
        experience_company = data.get("experience_company", None)
        experience_role = data.get("experience_role", None)
        experience_description = data.get("experience_description", None)
        experience_start_time = ResumeTools.convert_time(data.get("experience_start_time", ""))
        experience_end_time = ResumeTools.convert_time(data.get("experience_end_time", ""))

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            experience.profile = profile

        if title is not None:
            experience.title = title

        if description is not None:
            experience.description = description

        if experience_company is not None:
            experience.experience_company = experience_company

        if experience_role is not None:
            experience.experience_role = experience_role

        if experience_description is not None:
            experience.experience_description = experience_description

        if experience_start_time is not None:
            experience.experience_start_time = experience_start_time

        if experience_end_time is not None:
            experience.experience_end_time = experience_end_time

        experience.save()

        return (True, experience)

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
    def get_competence_obj(request, source: dict | str | None = None) -> tuple[bool, models.ResumeCompetence | str] | None:
        if isinstance(source, dict):
            success, comp_obj_or_error = ResumeTools.create_competence(request, source)
            if not success:
                return (False, comp_obj_or_error)  # type: ignore

            comp_obj: models.ResumeCompetence = comp_obj_or_error  # type: ignore
            return (True, comp_obj)

        if isinstance(source, str):
            comp_obj = ResumeTools.get_competence_from(source)  # type: ignore
            if comp_obj is None:
                return (False, f"Competence ID #{source} not found")

            return (True, comp_obj)

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
    def create_competence(request: HttpRequest, json: dict | None = None) -> tuple[bool, models.ResumeCompetence | str]:
        success, data_or_error = ResumeTools.get_competence_data(request, False, json)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        competence_name = data.get("competence_name", "")
        competence_level = data.get("competence_level", "")

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if not profile:
            return (False, "Profile not found")

        competence = models.ResumeCompetence.objects.create(profile=profile,
                                                            title=title,
                                                            description=description,
                                                            competence_name=competence_name,
                                                            competence_level=competence_level)

        return (True, competence)

    @staticmethod
    def edit_competence(request: HttpRequest, competence: models.ResumeCompetence) -> tuple[bool, models.ResumeCompetence | str]:
        success, data_or_error = ResumeTools.get_competence_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", None)
        title = data.get("title", None)
        description = data.get("description", None)
        competence_name = data.get("competence_name", None)
        competence_level = data.get("competence_level", None)

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            competence.profile = profile

        if title is not None:
            competence.title = title

        if description is not None:
            competence.description = description

        if competence_name is not None:
            competence.competence_name = competence_name

        if competence_level is not None:
            competence.competence_level = competence_level

        competence.save()

        return (True, competence)

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
    def get_course_obj(request, source: dict | str | None = None) -> tuple[bool, models.ResumeCourse | str] | None:
        if isinstance(source, dict):
            success, course_obj_or_error = ResumeTools.create_course(request, source)
            if not success:
                return (False, course_obj_or_error)  # type: ignore

            course_obj: models.ResumeCourse = course_obj_or_error  # type: ignore
            return (True, course_obj)

        if isinstance(source, str):
            course_obj = ResumeTools.get_course_from(source)  # type: ignore
            if course_obj is None:
                return (False, f"Course ID #{source} not found")

            return (True, course_obj)

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
    def create_course(request: HttpRequest, json: dict | None = None) -> tuple[bool, models.ResumeCourse | str]:
        success, data_or_error = ResumeTools.get_course_data(request, False, json)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        course_name = data.get("course_name", "")
        course_locale = data.get("course_locale", "")
        course_provider = data.get("course_provider", "")
        course_hours = data.get("course_hours", "")
        course_start_time = ResumeTools.convert_time(data.get("course_start_time", ""))
        course_end_time = ResumeTools.convert_time(data.get("course_end_time", ""))

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if not profile:
            return (False, "Profile not found")

        course = models.ResumeCourse.objects.create(profile=profile,
                                                    title=title,
                                                    description=description,
                                                    course_name=course_name,
                                                    course_locale=course_locale,
                                                    course_provider=course_provider,
                                                    course_hours=course_hours,
                                                    course_start_time=course_start_time,
                                                    course_end_time=course_end_time)

        return (True, course)

    @staticmethod
    def edit_course(request: HttpRequest, course: models.ResumeCourse) -> tuple[bool, models.ResumeCourse | str]:
        success, data_or_error = ResumeTools.get_course_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", None)
        title = data.get("title", None)
        description = data.get("description", None)
        course_name = data.get("course_name", None)
        course_locale = data.get("course_locale", None)
        course_provider = data.get("course_provider", None)
        course_hours = data.get("course_hours", None)
        course_start_time = ResumeTools.convert_time(data.get("course_start_time", ""))
        course_end_time = ResumeTools.convert_time(data.get("course_end_time", ""))

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            course.profile = profile

        if title is not None:
            course.title = title

        if description is not None:
            course.description = description

        if course_name is not None:
            course.course_name = course_name

        if course_locale is not None:
            course.course_locale = course_locale

        if course_provider is not None:
            course.course_provider = course_provider

        if course_hours is not None:
            course.course_hours = course_hours

        if course_start_time is not None:
            course.course_start_time = course_start_time

        if course_end_time is not None:
            course.course_end_time = course_end_time

        course.save()

        return (True, course)

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
    def get_reference_obj(request, source: dict | str | None = None) -> tuple[bool, models.ResumeReference | str] | None:
        if isinstance(source, dict):
            success, ref_obj_or_error = ResumeTools.create_reference(request, source)
            if not success:
                return (False, ref_obj_or_error)  # type: ignore

            ref_obj: models.ResumeReference = ref_obj_or_error  # type: ignore
            return (True, ref_obj)

        if isinstance(source, str):
            ref_obj = ResumeTools.get_reference_from(source)  # type: ignore
            if ref_obj is None:
                return (False, f"Reference ID #{source} not found")

            return (True, ref_obj)

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
    def create_reference(request: HttpRequest, json: dict | None = None) -> tuple[bool, models.ResumeReference | str]:
        success, data_or_error = ResumeTools.get_reference_data(request, False, json)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        reference_name = data.get("reference_name", "")
        reference_role = data.get("reference_role", "")
        reference_company = data.get("reference_company", "")
        reference_phone = data.get("reference_phone", "")
        reference_email = data.get("reference_email", "")

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if not profile:
            return (False, "Profile not found")

        reference = models.ResumeReference.objects.create(profile=profile,
                                                          title=title,
                                                          description=description,
                                                          reference_name=reference_name,
                                                          reference_role=reference_role,
                                                          reference_company=reference_company,
                                                          reference_phone=reference_phone,
                                                          reference_email=reference_email)

        return (True, reference)

    @staticmethod
    def edit_reference(request: HttpRequest, reference: models.ResumeReference) -> tuple[bool, models.ResumeReference | str]:
        success, data_or_error = ResumeTools.get_reference_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", None)
        title = data.get("title", None)
        description = data.get("description", None)
        reference_name = data.get("reference_name", None)
        reference_role = data.get("reference_role", None)
        reference_company = data.get("reference_company", None)
        reference_phone = data.get("reference_phone", None)
        reference_email = data.get("reference_email", None)

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            reference.profile = profile

        if title is not None:
            reference.title = title

        if description is not None:
            reference.description = description

        if reference_name is not None:
            reference.reference_name = reference_name

        if reference_role is not None:
            reference.reference_role = reference_role

        if reference_company is not None:
            reference.reference_company = reference_company

        if reference_phone is not None:
            reference.reference_phone = reference_phone

        if reference_email is not None:
            reference.reference_email = reference_email

        reference.save()

        return (True, reference)

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
    def get_graduation_obj(request, source: dict | str | None = None) -> tuple[bool, models.ResumeGraduation | str] | None:
        if isinstance(source, dict):
            success, grad_obj_or_error = ResumeTools.create_graduation(request, source)
            if not success:
                return (False, grad_obj_or_error)  # type: ignore

            grad_obj: models.ResumeGraduation = grad_obj_or_error  # type: ignore
            return (True, grad_obj)

        if isinstance(source, str):
            grad_obj = ResumeTools.get_graduation_from(source)  # type: ignore
            if grad_obj is None:
                return (False, f"Graduation ID #{source} not found")

            return (True, grad_obj)

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
    def create_graduation(request: HttpRequest, json: dict | None = None) -> tuple[bool, models.ResumeGraduation | str]:
        success, data_or_error = ResumeTools.get_graduation_data(request, False, json)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        graduation_type = data.get("graduation_type", "")
        graduation_period = data.get("graduation_period", "")
        graduation_start_time = ResumeTools.convert_time(data.get("graduation_start_time", ""))
        graduation_end_time = ResumeTools.convert_time(data.get("graduation_end_time", ""))

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if not profile:
            return (False, "Profile not found")

        graduation = models.ResumeGraduation.objects.create(profile=profile,
                                                            title=title,
                                                            description=description,
                                                            graduation_type=graduation_type,
                                                            graduation_period=graduation_period,
                                                            graduation_start_time=graduation_start_time,
                                                            graduation_end_time=graduation_end_time)

        return (True, graduation)

    @staticmethod
    def edit_graduation(request: HttpRequest, graduation: models.ResumeGraduation) -> tuple[bool, models.ResumeGraduation | str]:
        success, data_or_error = ResumeTools.get_graduation_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", None)
        title = data.get("title", None)
        description = data.get("description", None)
        graduation_type = data.get("graduation_type", None)
        graduation_period = data.get("graduation_period", None)
        graduation_start_time = ResumeTools.convert_time(data.get("graduation_start_time", ""))
        graduation_end_time = ResumeTools.convert_time(data.get("graduation_end_time", ""))

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            graduation.profile = profile

        if title is not None:
            graduation.title = title

        if description is not None:
            graduation.description = description

        if graduation_type is not None:
            graduation.graduation_type = graduation_type

        if graduation_period is not None:
            graduation.graduation_period = graduation_period

        if graduation_start_time is not None:
            graduation.graduation_start_time = graduation_start_time

        if graduation_end_time is not None:
            graduation.graduation_end_time = graduation_end_time

        graduation.save()

        return (True, graduation)

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
    def get_project_obj(request, source: dict | str | None = None) -> tuple[bool, models.ResumeProject | str] | None:
        if isinstance(source, dict):
            success, proj_obj_or_error = ResumeTools.create_project(request, source)
            if not success:
                return (False, proj_obj_or_error)  # type: ignore

            proj_obj: models.ResumeProject = proj_obj_or_error  # type: ignore
            return (True, proj_obj)

        if isinstance(source, str):
            proj_obj = ResumeTools.get_project_from(source)  # type: ignore
            if proj_obj is None:
                return (False, f"Project ID #{source} not found")

            return (True, proj_obj)

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
    def create_project(request: HttpRequest, json: dict | None = None) -> tuple[bool, models.ResumeProject | str]:
        success, data_or_error = ResumeTools.get_project_data(request, False, json)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        project_name = data.get("project_name", "")
        project_description = data.get("project_description", "")
        project_link = data.get("project_link", "")

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if not profile:
            return (False, "Profile not found")

        project = models.ResumeProject.objects.create(profile=profile,
                                                      title=title,
                                                      description=description,
                                                      project_name=project_name,
                                                      project_description=project_description,
                                                      project_link=project_link)

        return (True, project)

    @staticmethod
    def edit_project(request: HttpRequest, project: models.ResumeProject) -> tuple[bool, models.ResumeProject | str]:
        success, data_or_error = ResumeTools.get_project_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", None)
        title = data.get("title", None)
        description = data.get("description", None)
        project_name = data.get("project_name", None)
        project_description = data.get("project_description", None)
        project_link = data.get("project_link", None)

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            project.profile = profile

        if title is not None:
            project.title = title

        if description is not None:
            project.description = description

        if project_name is not None:
            project.project_name = project_name

        if project_description is not None:
            project.project_description = project_description

        if project_link is not None:
            project.project_link = project_link

        project.save()

        return (True, project)

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
    def get_link_obj(request, source: dict | str | None = None) -> tuple[bool, models.ResumeLink | str] | None:
        if isinstance(source, dict):
            success, link_obj_or_error = ResumeTools.create_link(request, source)
            if not success:
                return (False, link_obj_or_error)  # type: ignore

            link_obj: models.ResumeLink = link_obj_or_error  # type: ignore
            return (True, link_obj)

        if isinstance(source, str):
            link_obj = ResumeTools.get_link_from(source)  # type: ignore
            if link_obj is None:
                return (False, f"Link ID #{source} not found")

            return (True, link_obj)

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
    def create_link(request: HttpRequest, json: dict | None = None) -> tuple[bool, models.ResumeLink | str]:
        success, data_or_error = ResumeTools.get_link_data(request, False, json)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", 0)
        title = data.get("title", "")
        description = data.get("description", "")
        url = data.get("url", "")

        profile = UserProfile.objects.filter(pk=profile_pk).first()

        if not profile:
            return (False, "Profile not found")

        link = models.ResumeLink.objects.create(profile=profile,
                                                title=title,
                                                description=description,
                                                url=url)

        return (True, link)

    @staticmethod
    def edit_link(request: HttpRequest, link: models.ResumeLink) -> tuple[bool, models.ResumeLink | str]:
        success, data_or_error = ResumeTools.get_link_data(request, True)
        if not success:
            return (False, data_or_error)  # type: ignore

        data: dict = data_or_error  # type: ignore
        profile_pk = data.get("profile_pk", None)
        title = data.get("title", None)
        description = data.get("description", None)
        url = data.get("url", None)

        if profile_pk is not None:
            profile = UserProfile.objects.filter(pk=profile_pk).first()

            if not profile:
                return (False, "Profile not found")

            link.profile = profile

        if title is not None:
            link.title = title

        if description is not None:
            link.description = description

        if url is not None:
            link.url = url

        link.save()

        return (True, link)

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
        success, object_or_error = ResumeTools.create_resume(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeModel = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Resume created")

        serializer = serializers.ResumeModelSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_resume(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_resume_str)

        success, object_or_error = ResumeTools.edit_resume(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeModel = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Resume Updated")

        serializer = serializers.ResumeModelSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
                        description="Experience start date (ISO format [yyyy-MM-dd])"
                    ),
                    coreapi.Field(
                        name="experience_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience end date (ISO format [yyyy-MM-dd])"
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
                        description="Experience start date (ISO format [yyyy-MM-dd])"
                    ),
                    coreapi.Field(
                        name="experience_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Experience end date (ISO format [yyyy-MM-dd])"
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
        success, object_or_error = ResumeTools.create_experience(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeExperience = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Experience created")

        serializer = serializers.ExperienceSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_experience(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_experience_str)

        success, object_or_error = ResumeTools.edit_experience(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeExperience = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Experience Updated")

        serializer = serializers.ExperienceSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
        success, object_or_error = ResumeTools.create_competence(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeCompetence = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Competence created")

        serializer = serializers.CompetenceSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_competence(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_competence_str)

        success, object_or_error = ResumeTools.edit_competence(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeCompetence = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Competence Updated")

        serializer = serializers.CompetenceSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
                        description="Course start date (ISO format [yyyy-MM-dd])"
                    ),
                    coreapi.Field(
                        name="course_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course end date (ISO format [yyyy-MM-dd])"
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
                        description="Course start date (ISO format [yyyy-MM-dd])"
                    ),
                    coreapi.Field(
                        name="course_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Course end date (ISO format [yyyy-MM-dd])"
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
        success, object_or_error = ResumeTools.create_course(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeCourse = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Course created")

        serializer = serializers.CourseSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_course(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_course_str)

        success, object_or_error = ResumeTools.edit_course(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeCourse = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Course Updated")

        serializer = serializers.CourseSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
        success, object_or_error = ResumeTools.create_reference(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeReference = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Reference created")

        serializer = serializers.ReferenceSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_reference(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_reference_str)

        success, object_or_error = ResumeTools.edit_reference(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeReference = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Reference Updated")

        serializer = serializers.ReferenceSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
                        description="Graduation start date (ISO format [yyyy-MM-dd])"
                    ),
                    coreapi.Field(
                        name="graduation_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation end date (ISO format [yyyy-MM-dd])"
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
                        description="Graduation start date (ISO format [yyyy-MM-dd])"
                    ),
                    coreapi.Field(
                        name="graduation_end_time",
                        location='form',
                        required=False,
                        schema=coreschema.String(),
                        description="Graduation end date (ISO format [yyyy-MM-dd])"
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
        success, object_or_error = ResumeTools.create_graduation(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeGraduation = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Graduation created")

        serializer = serializers.GraduationSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_graduation(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_graduation_str)

        success, object_or_error = ResumeTools.edit_graduation(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeGraduation = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Graduation Updated")

        serializer = serializers.GraduationSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
        success, object_or_error = ResumeTools.create_project(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeProject = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Project created")

        serializer = serializers.ProjectSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_project(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_project_str)

        success, object_or_error = ResumeTools.edit_project(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeProject = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Project Updated")

        serializer = serializers.ProjectSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

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
        success, object_or_error = ResumeTools.create_link(request)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeLink = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_201_CREATED,
                                                          "Link created")

        serializer = serializers.LinkSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        editing_object = ResumeTools.get_link(request)

        if not editing_object:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
                                                self.not_found_link_str)

        success, object_or_error = ResumeTools.edit_link(request, editing_object)
        if not success:
            return self.generate_basic_response(status.HTTP_400_BAD_REQUEST, object_or_error)  # type: ignore

        model_object: models.ResumeLink = object_or_error  # type: ignore

        response_data = self.generate_basic_response_data(status.HTTP_200_OK,
                                                          "Link Updated")

        serializer = serializers.LinkSerializer(model_object, many=False)
        response_data['content'] = serializer.data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        link_model = ResumeTools.get_link(request)

        if link_model is not None:
            ResumeTools.delete_link(request, link_model)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
                                            self.not_found_link_str)
