from tools.image_funcs import get_image_path
from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField

from apps.base.models import BaseModel


class User(AbstractUser, BaseModel):
    profile_image = ImageField(upload_to=get_image_path, blank=True, null=True)
