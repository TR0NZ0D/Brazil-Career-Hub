from . import views
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from .tools.api_tools import generate_version, version, environment

app_name = 'api'

schema_url_patterns = [
    path('api/', include('api.urls'))
]

schema_view = get_schema_view(title='Job Finder - API',
                              description=f'API documentation [{version} - {environment}]',
                              version=generate_version(),
                              patterns=schema_url_patterns)

urlpatterns = [
    path('schema/', schema_view, name='api_schema'),
    path('status/', views.ApiStatus.as_view()),  # type: ignore
    path('version/', views.ApiVersion.as_view()),  # type: ignore
    path('token/', views.AuthToken.as_view()),  # type: ignore
    path('res_test/', views.ApiTesting.as_view())  # type: ignore
]
