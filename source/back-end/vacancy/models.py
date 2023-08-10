from django.db import models


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

    class Meta:
        verbose_name = 'Vacancy Address'
        verbose_name_plural = 'Vacancy Addresses'


class VacancyModel(models.Model):
    role = models.CharField(verbose_name="Role", max_length=255)
    description = models.TextField(verbose_name="Description")
    modality = models.CharField(verbose_name="Modality", max_length=255)
    created_at = models.DateTimeField(verbose_name="Created At",
                                      auto_now_add=True,
                                      editable=False)
    salary = models.IntegerField(verbose_name="Salary")
    address = models.ForeignKey(VacancyAddress,
                                verbose_name="Address",
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    resume = models.FileField(verbose_name="Resume",
                              upload_to='resumes/%Y/%m/%d')

    def __str__(self) -> str:
        return self.role

    class Meta:
        verbose_name = 'Job vacancy'
        verbose_name_plural = 'Job vacancies'
