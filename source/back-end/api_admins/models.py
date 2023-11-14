"""
api_admins/models.py

Created by: Gabriel Menezes de Antonio
"""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ApiAdmin(models.Model):
    """Model for api admin"""
    user = models.OneToOneField(User,  # type: ignore
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                help_text=(
                                    "The user that own this token. \
                                    Please check if user is admin before giving him a token."
                                ),
                                error_messages={"unique": "This user already has a token."})
    token = models.CharField(max_length=255,  # type: ignore
                             verbose_name="API Token",
                             unique=True,
                             blank=True,
                             null=True,
                             help_text=(
                                 "This is the API Authentication token, keep in production safe."
                             ),
                             error_messages={
                                 "unique": "This API token is already taken, please use another."
                             })

    def __str__(self) -> str:
        return f"{self.user.get_username()}'s API Admin account"

    class Meta:
        """Meta class for Api Admin model"""
        verbose_name = 'API Admin'
        verbose_name_plural = 'API Admins'
