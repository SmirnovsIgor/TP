from tools.image_funcs import get_image_path
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.base.models import BaseModel


class User(AbstractUser, BaseModel):
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    email = models.EmailField('email address', blank=False)
