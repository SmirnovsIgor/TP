from django.contrib.auth.models import AbstractUser
from apps.base.models import BaseModel

class User(AbstractUser, BaseModel):
    pass
