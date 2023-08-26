from django.db import models

from users.models import UserProfile


class ResumeExperiences(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True)
    experience_company = models.CharField("Experience company",
                                          blank=True,
                                          max_length=255)
    experience_role = models.CharField("Experience role",
                                       blank=True,
                                       max_length=255)
    experience_description = models.TextField("Experience description",
                                              blank=True)
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


class ResumeCompetences(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True)
    competency_name = models.CharField("Competency name",
                                       blank=True,
                                       max_length=255)
    competency_level = models.CharField("Competency level",
                                        blank=True,
                                        max_length=255)

    def __str__(self) -> str:
        return f"{self.profile.user.first_name}'s competency: {self.title}"  # type: ignore

    class Meta:
        verbose_name = 'Resume competency'
        verbose_name_plural = 'Resume competencies'


class ResumeCourses(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True)
    course_name = models.CharField("Course name",
                                   blank=True,
                                   max_length=255)
    course_locale = models.CharField("Course locale",
                                     blank=True,
                                     max_length=255)
    course_provider = models.CharField("Course provider",
                                       blank=True,
                                       max_length=255)
    course_hours = models.CharField("Course hours",
                                    blank=True,
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


class ResumeReferences(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True)
    reference_name = models.CharField("Reference name",
                                      blank=True,
                                      max_length=255)
    reference_role = models.CharField("Reference role",
                                      blank=True,
                                      max_length=255)
    reference_company = models.CharField("Reference company",
                                         blank=True,
                                         max_length=255)
    reference_phone = models.CharField("Reference Phone",
                                       blank=True,
                                       max_length=255)
    refecence_email = models.EmailField("Reference email",
                                        blank=True,
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
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True)
    graduation_type = models.CharField("Type",
                                       blank=True,
                                       max_length=150)
    graduation_period = models.CharField("Period",
                                         blank=True,
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


class ResumeProjects(models.Model):
    profile = models.ForeignKey(UserProfile,
                                verbose_name="Profile",
                                on_delete=models.CASCADE)
    title = models.CharField("Title",
                             blank=True,
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True)
    project_name = models.CharField("Project name",
                                    blank=True,
                                    max_length=255)
    project_description = models.TextField("Project description",
                                           blank=True)
    project_link = models.URLField("Project link",
                                   blank=True,
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
                             max_length=255)
    description = models.CharField(verbose_name="Company's username",
                                   blank=True,
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
                             max_length=255)
    description = models.TextField("Description",
                                   blank=True)
    experiences = models.ManyToManyField(ResumeExperiences,
                                         blank=True,
                                         verbose_name="Experiences")
    competences = models.ManyToManyField(ResumeCompetences,
                                         blank=True,
                                         verbose_name="Competences")
    courses = models.ManyToManyField(ResumeCourses,
                                     blank=True,
                                     verbose_name="Courses")
    references = models.ManyToManyField(ResumeReferences,
                                        blank=True,
                                        verbose_name="References")
    graduations = models.ManyToManyField(ResumeGraduation,
                                         blank=True,
                                         verbose_name="Graduations")
    projects = models.ManyToManyField(ResumeProjects,
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