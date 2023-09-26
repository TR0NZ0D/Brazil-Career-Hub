from django.db import models

from users.models import UserProfile


class ResumeExperience(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             null=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    experience_company = models.CharField("Experience company",
                                          blank=True,
                                          null=True,
                                          max_length=255)
    experience_role = models.CharField("Experience role",
                                       blank=True,
                                       null=True,
                                       max_length=255)
    experience_description = models.TextField("Experience description",
                                              blank=True,
                                              null=True)
    experience_start_time = models.DateField("Experience start time",
                                             auto_now=False,
                                             auto_now_add=False,
                                             blank=True,
                                             null=True)
    experience_end_time = models.DateField("Experience end time",
                                           auto_now=False,
                                           auto_now_add=False,
                                           blank=True,
                                           null=True)

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s experience: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume experience'
        verbose_name_plural = 'Resume experiencies'


class ResumeCompetence(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             null=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    competence_name = models.CharField("Competence name",
                                       blank=True,
                                       null=True,
                                       max_length=255)
    competence_level = models.CharField("Competence level",
                                        blank=True,
                                        null=True,
                                        max_length=255)

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s competence: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume competence'
        verbose_name_plural = 'Resume competencies'


class ResumeCourse(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             null=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    course_name = models.CharField("Course name",
                                   blank=True,
                                   null=True,
                                   max_length=255)
    course_locale = models.CharField("Course locale",
                                     blank=True,
                                     null=True,
                                     max_length=255)
    course_provider = models.CharField("Course provider",
                                       blank=True,
                                       null=True,
                                       max_length=255)
    course_hours = models.CharField("Course hours",
                                    blank=True,
                                    null=True,
                                    max_length=255)
    course_start_time = models.DateField("Course start time",
                                         auto_now=False,
                                         auto_now_add=False,
                                         blank=True,
                                         null=True)
    course_end_time = models.DateField("Course end time",
                                       auto_now=False,
                                       auto_now_add=False,
                                       blank=True,
                                       null=True)

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s course: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume course'
        verbose_name_plural = 'Resume courses'


class ResumeReference(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             null=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    reference_name = models.CharField("Reference name",
                                      blank=True,
                                      null=True,
                                      max_length=255)
    reference_role = models.CharField("Reference role",
                                      blank=True,
                                      null=True,
                                      max_length=255)
    reference_company = models.CharField("Reference company",
                                         blank=True,
                                         null=True,
                                         max_length=255)
    reference_phone = models.CharField("Reference Phone",
                                       blank=True,
                                       null=True,
                                       max_length=255)
    reference_email = models.EmailField("Reference email",
                                        blank=True,
                                        null=True,
                                        max_length=255)

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s reference: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume reference'
        verbose_name_plural = 'Resume references'


class ResumeGraduation(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             null=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    graduation_type = models.CharField("Type",
                                       blank=True,
                                       null=True,
                                       max_length=150)
    graduation_period = models.CharField("Period",
                                         blank=True,
                                         null=True,
                                         max_length=150)
    graduation_start_time = models.DateField("Graduation start time",
                                             auto_now=False,
                                             auto_now_add=False,
                                             blank=True,
                                             null=True)
    graduation_end_time = models.DateField("Graduation end time",
                                           auto_now=False,
                                           auto_now_add=False,
                                           blank=True,
                                           null=True)

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s graduation: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume graduation'
        verbose_name_plural = 'Resume graduations'


class ResumeProject(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    project_name = models.CharField("Project name",
                                    blank=True,
                                    null=True,
                                    max_length=255)
    project_description = models.TextField("Project description",
                                           blank=True,
                                           null=True)
    project_link = models.URLField("Project link",
                                   blank=True,
                                   null=True,
                                   max_length=255)

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s project: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume project'
        verbose_name_plural = 'Resume projects'


class ResumeLink(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Title",
                             null=True,
                             max_length=255)
    description = models.CharField(verbose_name="Company's username",
                                   blank=True,
                                   null=True,
                                   max_length=255)
    url = models.URLField(verbose_name="Website URL")

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s link: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume link'
        verbose_name_plural = 'Resume links'


class ResumeModel(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             null=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True,
                                   null=True)
    experiences = models.ManyToManyField(ResumeExperience,
                                         blank=True,
                                         verbose_name="Experiences")
    competencies = models.ManyToManyField(ResumeCompetence,
                                          blank=True,
                                          verbose_name="Competencies")
    courses = models.ManyToManyField(ResumeCourse,
                                     blank=True,
                                     verbose_name="Courses")
    references = models.ManyToManyField(ResumeReference,
                                        blank=True,
                                        verbose_name="References")
    graduations = models.ManyToManyField(ResumeGraduation,
                                         blank=True,
                                         verbose_name="Graduations")
    projects = models.ManyToManyField(ResumeProject,
                                      blank=True,
                                      verbose_name="Projects")
    links = models.ManyToManyField(ResumeLink,
                                   blank=True,
                                   verbose_name="links")
    created_at = models.DateTimeField("Created at",
                                      auto_now_add=True,
                                      editable=False)

    def __str__(self) -> str:
        describer = f"#{self.pk}" if not self.title else self.title
        return f"{self.profile.user.first_name}'s resume: {describer}"  # type: ignore

    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
