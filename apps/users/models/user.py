from datetime import date
from tools.image_funcs import get_image_path
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.base.models import BaseAbstractModel


class User(AbstractUser, BaseAbstractModel):
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    email = models.EmailField('email address', blank=False, null=False)
    first_name = models.CharField('first name', max_length=30, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)
    date_of_birth = models.DateField('date of birth', blank=True, null=False, default=date.today)
