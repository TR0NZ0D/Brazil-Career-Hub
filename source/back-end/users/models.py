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
                                 DEFAULT_SECONDARY_COLOR, GENDERS,
                                 SUPPORTED_LANGUAGES)

User = get_user_model()


class UserBadges(models.Model):
    """User badges model"""
    name = models.CharField(verbose_name="Name",  # type: ignore
                            max_length=20,
                            help_text="Badge name")
    description = models.TextField(verbose_name="Description",  # type: ignore
                                   max_length=255,
                                   help_text="Badge description")
    color = models.CharField(verbose_name="Color",  # type: ignore
                             max_length=7,
                             # TODO: Change default color after defining color pallete
                             default="#c7c5c5",
                             help_text="Badge color")

    def __str__(self) -> str:
        return self.name.__str__()

    class Meta:
        """Meta data for user badges"""
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

    def clean(self) -> None:
        error_messages = {}

        if not self.name:
            error_messages["name"] = 'Please name your badge.'
            raise ValidationError(error_messages)

        badge = UserBadges.objects.all().filter(name=self.name).first()

        if badge:
            if (badge.name == self.name) and (self.pk != badge.pk):
                error_messages['name'] = f"Badge with name '{self.name}' already exists."

            if (badge.color == self.color) and (self.pk != badge.pk):
                error_messages['color'] = f"Badge with color '{self.color}' already exists."

        if not self.description:
            error_messages['description'] = 'Please describe your badge'

        if not self.color:
            error_messages['color'] = 'Please chose a color for your badge'

        if error_messages:
            raise ValidationError(error_messages)


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
    language = models.CharField(verbose_name="Language",  # type: ignore
                                max_length=5,
                                choices=SUPPORTED_LANGUAGES,
                                default='pt-br',
                                help_text="This is the user's language, \
                                    can be used to communicate and / or translate the website")
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
    badges = models.ManyToManyField(UserBadges,  # type: ignore
                                    verbose_name="Badges",
                                    editable=True,
                                    blank=True,
                                    help_text="List of badges that this user has aquired.")

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
