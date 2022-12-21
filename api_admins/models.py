from django.db import models
from django.contrib.auth.models import User


class ApiAdmin(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                help_text=("The user that own this token. Please check if user is admin before giving him a token."),
                                error_messages={"unique": "This user already has a token."})
    token = models.CharField(max_length=255,
                             verbose_name="API Token",
                             unique=True,
                             blank=True,
                             null=True,
                             help_text=("This is the API Authentication token, keep in production safe."),
                             error_messages={"unique": "This API token is already taken, please use another."})

    def __str__(self) -> str:
        return f"{self.user.get_username()}'s API Admin account"

    class Meta:
        verbose_name = 'API Admin'
        verbose_name_plural = 'API Admins'
