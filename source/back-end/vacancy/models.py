from typing import Any
from django.db import models
from company.models import CompanyAccountModel
from resumes.models import ResumeModel


class VacancyAddress(models.Model):
    title = models.CharField(verbose_name="Title",
                             max_length=255)
    address = models.CharField(verbose_name="Address",
                               max_length=255)
    number = models.PositiveIntegerField(verbose_name="Number",
                                         blank=True,
                                         null=True)

    def __str__(self) -> str:
        return self.title

    def __getattribute__(self, __name: str) -> Any:
        if __name == "serialize":
            return {
                "title": self.title,
                "address": self.address,
                "number": self.number
            }
        return super().__getattribute__(__name)

    class Meta:
        verbose_name = 'Vacancy Address'
        verbose_name_plural = 'Vacancy Addresses'


class VacancyModel(models.Model):
    created_by = models.ForeignKey(CompanyAccountModel,
                                   verbose_name="Created by",
                                   on_delete=models.CASCADE)
    role = models.CharField(verbose_name="Role", max_length=255)
    description = models.TextField(verbose_name="Description")
    modality = models.CharField(verbose_name="Modality", max_length=255)
    created_at = models.DateTimeField(verbose_name="Created At",
                                      auto_now_add=True,
                                      editable=False)
    salary = models.PositiveIntegerField(verbose_name="Salary")
    address = models.ForeignKey(VacancyAddress,
                                verbose_name="Address",
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    resumes = models.ManyToManyField(ResumeModel,
                                     verbose_name="Resumes",
                                     blank=True)

    def __str__(self) -> str:
        return self.role

    class Meta:
        verbose_name = 'Job vacancy'
        verbose_name_plural = 'Job vacancies'
