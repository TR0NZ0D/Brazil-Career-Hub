from django.db import models
from django.contrib.auth.models import User


class ApiAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    token = models.CharField(max_length=255, verbose_name="API Token", unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.get_username()}'s API Admin account"

    class Meta:
        verbose_name = 'API Admin'
        verbose_name_plural = 'API Admins'
