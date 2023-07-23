"""
company/models.py

Created by: Gabriel Menezes de Antonio
"""

from django.db import models
from django.utils.text import slugify

from api.tools.constants import LEGAL_NATURE, REGISTRATION_STATUS


class CompanyAccountModel(models.Model):
    """Model for company account"""
    cnpj = models.CharField(verbose_name="CNPJ",  # type: ignore
                            unique=True,
                            max_length=14,
                            help_text="The company's CNPJ",
                            error_messages={
                                "unique": "A company with this CNPJ is already registered"
                            })
    corporate_name = models.CharField(verbose_name="Corporate Name",  # type: ignore
                                      max_length=100,
                                      help_text="The company's corporate name")
    registration_status = models.CharField(verbose_name="Registration Status",  # type: ignore
                                           max_length=1,
                                           choices=REGISTRATION_STATUS,
                                           default='1',
                                           help_text="Company's registration status")
    fantasy_name = models.CharField(verbose_name="Fantasy Name",  # type: ignore
                                    max_length=60,
                                    help_text="Company's fantasy name")
    cnae = models.IntegerField(verbose_name="CNAE",  # type: ignore
                               help_text="Company's CNAE code")
    legal_nature = models.CharField(verbose_name="Legal Nature",  # type: ignore
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
        return f"{self.fantasy_name}'s company account"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not self.slug:
            try:
                first_fantasy_name = self.fantasy_name.split(" ")[0]
            except IndexError:
                first_fantasy_name = self.fantasy_name

            self.slug = str(
                slugify(f'{first_fantasy_name}-{self.pk}'))

        super().save(*args, **kwargs)

    class Meta:
        """Meta class for company account model"""
        verbose_name = 'Company Account'
        verbose_name_plural = 'Company Accounts'


class CompanyAddress(models.Model):
    title = models.CharField(verbose_name="Title",
                             max_length=255)
    address = models.CharField(verbose_name="Address",
                               max_length=255)
    number = models.PositiveIntegerField(verbose_name="Number",
                                         blank=True,
                                         null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        """Meta class for company account model"""
        verbose_name = 'Company Address'
        verbose_name_plural = 'Company Addresses'


class CompanySocialMedia(models.Model):
    title = models.CharField(verbose_name="Title",
                             max_length=255)
    url = models.URLField(verbose_name="Website URL")
    username = models.CharField(verbose_name="Company's username",
                                max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        """Meta class for company account model"""
        verbose_name = 'Company Social media Account'
        verbose_name_plural = 'Company Social media Accounts'


class CompanyProfileModel(models.Model):
    company_account = models.OneToOneField(CompanyAccountModel,  # type: ignore
                                           verbose_name="Company Account",
                                           on_delete=models.CASCADE,
                                           help_text=(
                                               "The company account related to this profile"),
                                           error_messages={"unique": "Company already has a profile."})
    address = models.ManyToManyField(CompanyAddress,
                                     blank=True,
                                     verbose_name="Address")
    contact = models.CharField(verbose_name="Contact",
                               max_length=255,
                               null=True,
                               blank=True,
                               help_text="The company contact information i.e. an email or phone number.")
    creation_date = models.DateField(verbose_name="Creation Date",  # type: ignore
                                     auto_now=False,
                                     auto_now_add=False,
                                     blank=True,
                                     null=True,
                                     help_text="This is the company's creation date")
    financial_capital = models.FloatField(verbose_name="Financial capital",  # type: ignore
                                          null=True,
                                          blank=True)
    employees = models.PositiveIntegerField(verbose_name="Company's employee number",  # type: ignore
                                            null=True,
                                            blank=True)
    site_url = models.URLField(verbose_name="Company's website URL",
                               blank=True,
                               null=True)
    social_media = models.ManyToManyField(CompanySocialMedia,
                                          blank=True,
                                          verbose_name="Company's social media accounts")

    def __str__(self) -> str:
        return f"{self.company_account.fantasy_name}'s company profile"

    class Meta:
        """Meta class for company account model"""
        verbose_name = 'Company Profile'
        verbose_name_plural = 'Company Profiles'
