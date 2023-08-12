# import coreapi
# import coreschema

# from django.core.exceptions import ValidationError
# from rest_framework import status
# from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema

# from api.tools.api_tools import description_generator
from api.views import Base
# from .serializers import ResumeModelSerializer
# from . import models


class ResumeSchema(AutoSchema):
    pass


class Resume(Base):
    pass
