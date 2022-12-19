from . import views
from django.urls import path, include
from django.views.generic import TemplateView
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

swagger_view = TemplateView.as_view(template_name='api/swagger-ui.html')

urlpatterns = [
    path('docs', swagger_view),
    path('', schema_view, name='api_schema'),
    path('status/', views.ApiStatus.as_view()),
    path('version/', views.ApiVersion.as_view())
]
