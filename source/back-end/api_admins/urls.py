from . import views
from django.urls import path

app_name = 'api_admins'


urlpatterns = [
    # ========== Token ========== #
    path('token/', views.BaseAuthToken.as_view()),  # type: ignore
]
