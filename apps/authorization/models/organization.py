from tools.image_funcs import get_image_path
from django.db import models
from apps.base.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=False)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
