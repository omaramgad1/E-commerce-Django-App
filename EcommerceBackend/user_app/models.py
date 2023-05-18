from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _


def validate_image(image):
    # Open the image file using PIL
    img = Image.open(image)

    # Check the file size
    max_size = 5 * 1024 * 1024  # 5 MB
    if image.size > max_size:
        raise ValidationError('Image size should be less than 5MB.')

    # Check the file format
    allowed_formats = ('jpeg', 'jpg', 'png', 'gif')
    if img.format.lower() not in allowed_formats:
        raise ValidationError('Only JPG, PNG, and GIF images are allowed.')


def validate_date_of_birth(value):
    today = date.today()
    age_limit = timedelta(days=365*12)
    if value > today:
        raise ValidationError('Date of birth cannot be in the future.')
    elif today - value < age_limit:
        raise ValidationError('You must be at least 12 years old to register.')


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, password2=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            # first_name=first_name,
            # last_name=last_name,
            # phone=phone,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, password2=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, password2, **extra_fields)

    def create_superuser(self, email, password=None, password2=None, ** extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser has to have the is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "superuser has to have the is_superuser being True")

        return self._create_user(email, password, password2,  **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(db_index=True, unique=True, max_length=254)

    # null=True, blank=True
    date_of_birth = models.DateField(
        null=True, blank=True,   validators=[validate_date_of_birth])
    phone = PhoneNumberField()
    profileImgUrl = models.ImageField(
        upload_to='profileImages/', blank=True, validators=[validate_image])  #
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # must needed, otherwise you won't be able to loginto django-admin.
    is_staff = models.BooleanField(default=False)
    # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True)
    # this field we inherit from PermissionsMixin.
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
# 'first_name', 'last_name',, 'phone'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
