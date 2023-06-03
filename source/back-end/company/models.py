"""
company/models.py

Created by: Gabriel Menezes de Antonio
"""

from django.db import models
from django.utils.text import slugify

from api.tools.constants import REGISTRATION_STATUS, LEGAL_NATURE


class CompanyAccountModel(models.Model):
    """Model for company account"""
    cnpj = models.CharField(verbose_name="CNPJ",  # type: ignore
                            unique=True,
                            max_length=14,
                            help_text="The company's CNPJ",
                            error_messages={
                                "unique": "A company with this CNPJ is already registered"
                            })
    razao_social = models.CharField(verbose_name="Corporate Name",  # type: ignore
                                    max_length=100,
                                    help_text="The company's corporate name")
    situacao_cadastral = models.CharField(verbose_name="Registration Status",  # type: ignore
                                          max_length=1,
                                          choices=REGISTRATION_STATUS,
                                          default='1',
                                          help_text="Company's registration status")
    nome_fantasia = models.CharField(verbose_name="Fantasy Name",  # type: ignore
                                     max_length=60,
                                     help_text="Company's fantasy name")
    cnae = models.IntegerField(verbose_name="CNAE",  # type: ignore
                               help_text="Company's CNAE code")
    natureza_juridica = models.CharField(verbose_name="Legal Nature",  # type: ignore
                                         max_length=6,
                                         choices=LEGAL_NATURE,
                                         default='EI',
                                         help_text="Company's Legal Nature")
    slug = models.SlugField(verbose_name="Company's Slug",  # type: ignore
                            unique=True,
                            null=True,
                            blank=True,
                            editable=False,
                            help_text="This is a unique field used to reference each company. \
                                This is auto generated.",
                            error_messages={"unique": "Slug is already owned by another company. \
                                Please use another"})

    def __str__(self) -> str:
        return f"{self.nome_fantasia}'s company account"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not self.slug:
            try:
                first_fantasy_name = self.nome_fantasia.split(" ")[0]
            except IndexError:
                first_fantasy_name = self.nome_fantasia

            self.slug = str(
                slugify(f'{first_fantasy_name}-{self.pk}'))

        super().save(*args, **kwargs)

    class Meta:
        """Meta class for company account model"""
        verbose_name = 'Company Account'
        verbose_name_plural = 'Company Accounts'
