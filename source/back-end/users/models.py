"""
users/models.py

Created by: Gabriel Menezes de Antonio
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from api.tools.api_tools import resize_image
from api.tools.constants import (DEFAULT_COVER_COLOR, DEFAULT_PRIMARY_COLOR,
                                 DEFAULT_SECONDARY_COLOR, GENDERS)

User = get_user_model()


class UserProfileLanguages(models.Model):
    language = models.CharField(verbose_name="Language",  # type: ignore
                                max_length=500)

    def __str__(self) -> str:
        return self.language

    class Meta:
        """Meta data for user profile"""
        verbose_name = 'Language'
        verbose_name_plural = "Languages"


class UserProfile(models.Model):
    """Model for user profile"""
    user = models.OneToOneField(User,  # type: ignore
                                verbose_name="User",
                                on_delete=models.CASCADE,
                                help_text=(
                                    "The User account related to this profile"),
                                error_messages={"unique": "User already has a profile."})
    tag = models.CharField(verbose_name="Tag",  # type: ignore
                           max_length=50,
                           null=True,
                           blank=True,
                           unique=True,
                           editable=False,
                           help_text=(
                               "This is the user's tag, is the same as its ID. \
                                This is auto-generated"),
                           error_messages={"unique": \
                                           "Tag is already owned by another user. \
                                            Please use another"})
    age = models.PositiveIntegerField(verbose_name="Age",  # type: ignore
                                      null=True,
                                      blank=True,
                                      help_text="This is the user's age, \
                                        calculated by its birth date.")
    birth_date = models.DateField(verbose_name="Birth Date",  # type: ignore
                                  auto_now=False,
                                  auto_now_add=False,
                                  blank=True,
                                  null=True,
                                  help_text="This is the user's birth date, \
                                    used for calculating its age")
    biography = models.TextField(verbose_name="Biography",  # type: ignore
                                 max_length=200,
                                 blank=True,
                                 null=True,
                                 help_text="This is the user's bio, \
                                    a quick description about them.")
    company = models.CharField(verbose_name="Company",  # type: ignore
                               max_length=100,
                               blank=True,
                               null=True,
                               help_text="This is the user's company, \
                                if working anywhere.")
    locale = models.CharField(verbose_name="Locale",  # type: ignore
                              max_length=80,
                              blank=True,
                              null=True,
                              help_text="This is the user's locale, \
                                used to filter by city.")
    nationality = models.CharField(verbose_name="Nationality",  # type: ignore
                                   max_length=80,
                                   help_text="This is the user's nationality.")
    cpf = models.CharField(verbose_name="CPF",  # type: ignore
                           null=True,
                           blank=True,
                           max_length=11,
                           help_text="User's CPF")
    phone_number = models.CharField(verbose_name="Phone Number",  # type: ignore
                                    null=True,
                                    blank=True,
                                    max_length=30,
                                    help_text="User's phone number")
    twitter_username = models.CharField(verbose_name="Twitter Username",  # type: ignore
                                        null=True,
                                        blank=True,
                                        max_length=15,
                                        help_text="User's Twitter account username")
    facebook_username = models.CharField(verbose_name="Facebook Username",  # type: ignore
                                         null=True,
                                         blank=True,
                                         max_length=50,
                                         help_text="User's Facebook account username")
    linkedin_username = models.CharField(verbose_name="LinkedIn Username",  # type: ignore
                                         null=True,
                                         blank=True,
                                         max_length=60,
                                         help_text="User's LinkedIn account username")
    instagram_username = models.CharField(verbose_name="Instagram Username",  # type: ignore
                                          null=True,
                                          blank=True,
                                          max_length=30,
                                          help_text="User's Instagram account username")
    website = models.URLField(verbose_name="Website",  # type: ignore
                              max_length=200,
                              blank=True,
                              null=True,
                              help_text="This is the user's website")
    image = models.ImageField(verbose_name="",  # type: ignore
                              upload_to='users/%Y/%m/%d',
                              default='defaults/person-8x.png',
                              help_text=("User's profile picture"),
                              null=True,
                              blank=True)
    email_confirmed = models.BooleanField(verbose_name="Email Confirmed",  # type: ignore
                                          default=False,
                                          help_text="Boolean value if user \
                                            has confirmed its email address")
    slug = models.SlugField(verbose_name="Slug",  # type: ignore
                            unique=True,
                            null=True,
                            blank=True,
                            editable=False,
                            help_text="This is a unique field used to reference each user. \
                                This is auto generated.",
                            error_messages={"unique": "Slug is already owned by another user. \
                                Please use another"})
    recovery_key = models.CharField(verbose_name="Recovery Key",  # type: ignore
                                    max_length=25,
                                    null=True,
                                    blank=True,
                                    editable=False,
                                    help_text="This is the user's recovery key \
                                        used in password and account recovery process.")
    languages = models.ManyToManyField(UserProfileLanguages,
                                       blank=True)
    gender = models.CharField(verbose_name="Gender",  # type: ignore
                              max_length=2,
                              choices=GENDERS,
                              default='NI',
                              help_text="This is the user gender, \
                                it's optional and defaults to NI.")
    cover_color = models.CharField(verbose_name="Cover Color",  # type: ignore
                                   max_length=7,
                                   default=DEFAULT_COVER_COLOR,
                                   help_text="This is the profile page's cover color, \
                                    can be customized by the user. Field uses HEX colors")
    primary_color = models.CharField(verbose_name="Primary Color",  # type: ignore
                                     max_length=7,
                                     default=DEFAULT_PRIMARY_COLOR,
                                     help_text="This is the user's primary color, \
                                        can be used in the website and can be customized \
                                            by the user. Field uses HEX colors")
    secondary_color = models.CharField(verbose_name="Secondary Color",  # type: ignore
                                       max_length=7,
                                       default=DEFAULT_SECONDARY_COLOR,
                                       help_text="This is the user's secondary color, \
                                        can be used in the website and can be customized \
                                            by the user. Field uses HEX colors")
    banned = models.BooleanField(verbose_name="Banned",  # type: ignore
                                 default=False,
                                 help_text="Boolean field that indicates if this user \
                                    has being banned.")
    must_reset_password = models.BooleanField(verbose_name="Must Reset Password",  # type: ignore
                                              default=False,
                                              help_text="Boolean field that indicates if \
                                                this user must reset its password before \
                                                    logging in.")

    def __str__(self) -> str:
        return f"{self.user.get_username()}'s profile"

    class Meta:
        """Meta data for user profile"""
        verbose_name = 'Profile'
        verbose_name_plural = "Profiles"

    def clean(self) -> None:
        error_messages = {}

        if self.age and self.birth_date:
            current_year = datetime.now().year
            birth_year: int | str = self.birth_date.strftime('%Y')
            try:
                birth_year = int(birth_year)
            except ValueError:
                birth_year = current_year - self.age

            if not isinstance(birth_year, int):
                error_string = "Internal error: birth_year is not an integer"
                error_messages['age'] = error_string
                error_messages['birth_date'] = error_string

            if (current_year - int(birth_year)) != self.age:
                error_string = "Age and birth date are incompatible."
                error_messages['age'] = error_string
                error_messages['birth_date'] = error_string

        if error_messages:
            raise ValidationError(error_messages)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = str(
                slugify(f'{self.user.get_username()}-{self.user.pk}'))

        if not self.tag:
            self.tag = self.user.pk

        if not self.age and self.birth_date:
            current_year = datetime.today().year
            birth_year: int | str = self.birth_date.strftime("%Y")
            try:
                birth_year = int(birth_year)
            except ValueError:
                birth_year = 2000
            self.age = current_year - birth_year

        if not self.birth_date and self.age:
            current_year = datetime.today().year
            birth_year = current_year - self.age
            birth_date = datetime.fromisocalendar(int(birth_year), week=1, day=1)
            self.birth_date = birth_date

        super().save(*args, **kwargs)

        max_img_width = 1092

        if self.image:
            resize_image(self.image, max_img_width)


class BannedUsers(models.Model):
    """Banned users model"""
    user = models.OneToOneField(User,  # type: ignore
                                verbose_name="User",
                                on_delete=models.CASCADE,
                                help_text="Banned user account")
    profile = models.OneToOneField(UserProfile,  # type: ignore
                                   verbose_name="Profile",
                                   on_delete=models.CASCADE,
                                   help_text="Banned user profile")
    reason = models.TextField(verbose_name="Reason",  # type: ignore
                              max_length=2000,
                              help_text="Ban reason")
    responsible = models.ForeignKey(User,  # type: ignore
                                    verbose_name="Responsible",
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name="ban_responsible",
                                    help_text="Admin responsible for banning the user")
    date = models.DateTimeField(verbose_name="Date",  # type: ignore
                                auto_now_add=True,
                                editable=False,
                                help_text="Date when the ban occurred")
    ip = models.GenericIPAddressField(verbose_name="IP",  # type: ignore
                                      protocol="both",
                                      help_text="Banned IP address")

    def __str__(self) -> str:
        return f"{self.user.get_username()}'s ban"

    class Meta:
        """Meta data for banned users"""
        verbose_name = 'Ban'
        verbose_name_plural = 'Bans'
