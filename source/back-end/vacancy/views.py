# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.schemas.coreapi import AutoSchema

# from api.tools.api_tools import description_generator
# from api.views import Base
# from .serializers import VacancyModelSerializer
# import coreapi
# import coreschema


# # =================== Vacancy =================== #
# class VacancySchema(AutoSchema):
#     def get_description(self, path: str, method: str) -> str:
#         authorization_info = """
# ## Authorization:

# **Type:** Bearer
# """
#         match method:
#             case 'GET':
#                 responses = {
#                     "200": {
#                         'description': 'OK',
#                         'reason': 'User logged out successfully'
#                     },
#                     "500": {
#                         'description': 'INTERNAL SERVER ERROR',
#                         'reason': 'Something went wrong'
#                     }
#                 }
#                 return description_generator(title="logout an user",
#                                              description=authorization_info,
#                                              responses=responses)
#             case 'POST':
#                 responses = {
#                     "200": {
#                         'description': 'OK',
#                         'reason': 'User authenticated and logged in successfully'
#                     },
#                     "202": {
#                         'description': 'ACCEPTED',
#                         'reason': 'User authenticated successfully, but, need to change password'
#                     },
#                     "400": {
#                         'description': "BAD REQUEST",
#                         'reason': 'Invalid request body'
#                     },
#                     "403": {
#                         'description': 'FORBIDDEN',
#                         'reason': 'Authentication failed'
#                     },
#                     "404": {
#                         'description': 'NOT FOUND',
#                         'reason': 'User account not found'
#                     },
#                     "423": {
#                         'description': 'LOCKED',
#                         'reason': 'User account can\'t be accessed due to a ban or other issue'
#                     },
#                     "500": {
#                         'description': 'INTERNAL SERVER ERROR',
#                         'reason': 'Something went wrong'
#                     }
#                 }
#                 return description_generator(title="Authenticate and login an user",
#                                              description=authorization_info,
#                                              responses=responses)
#             case _:
#                 return ''

#     def get_path_fields(self, path: str, method: str) -> list[coreapi.Field]:
#         match method:
#             case 'POST':
#                 return [
#                     coreapi.Field(
#                         name="username",
#                         location="form",
#                         required=True,
#                         schema=coreschema.String(),
#                         description="User's account username"
#                     ),
#                     coreapi.Field(
#                         name="password",
#                         location='form',
#                         required=True,
#                         schema=coreschema.String(),
#                         description="User's account password"
#                     )
#                 ]
#             case _:
#                 return []


# class Vacancy(Base):
#     """Authenticate user"""

#     schema = UserAuthenticationSchema()

#     def get(self, request):
#         """Get request"""

#         return self.generate_basic_response(status.HTTP_200_OK, "Logged out")

#     def post(self, request):
#         """Post request"""
#         username = request.data.get('username', None)
#         password = request.data.get('password', None)

#         if username is None or password is None:
#             return self.generate_basic_response(status.HTTP_400_BAD_REQUEST,
#                                                 "Username or password not found")

#         if request.user.is_authenticated:
#             return self.generate_basic_response(status.HTTP_409_CONFLICT,
#                                                 "An user is already logged in")

#         user = User.objects.all().filter(username=username).first()

#         if user is None:
#             return self.generate_basic_response(status.HTTP_404_NOT_FOUND,
#                                                 "No account found with this username")

#         authenticated_user = authenticate(request, username=username, password=password)

#         if authenticated_user is None:
#             return self.generate_basic_response(status.HTTP_403_FORBIDDEN,
#                                                 "Authentication failed, check your credentials")

#         profile = models.UserProfile.objects.all().filter(user=authenticated_user).first()

#         if profile is None:
#             return self.generate_basic_response(status.HTTP_500_INTERNAL_SERVER_ERROR,
#                                                 "User profile not found")

#         if profile.banned:
#             return self.generate_basic_response(status.HTTP_423_LOCKED,
#                                                 "User's account is banned")

#         if profile.must_reset_password:
#             data = self.generate_basic_response_data(status.HTTP_202_ACCEPTED,
#                                                      "User must change password before logging in")
#             serializer = serializers.UserProfileSerializer(profile)
#             data['content'] = serializer.data
#             return Response(data=data, status=data.get('status', status.HTTP_202_ACCEPTED))

#         data = self.generate_basic_response_data(status.HTTP_200_OK,
#                                                  "Logged in successfully")
#         serializer = serializers.UserProfileSerializer(profile)
#         data['content'] = serializer.data
#         return Response(data=data, status=data.get('status', status.HTTP_200_OK))
