from django.db import models

from apps.events.models import Event
from apps.users.models import User
from tools.image_funcs import get_image_path
from apps.base.models import BaseAbstractModel


class Organization(BaseAbstractModel):
    name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    @property
    def all_events(self):
        return Event.objects.filter(organizer_id=self.id)

    @property
    def all_members(self):
        return User.objects.filter(membership__organization__id=self.id)

    def __str__(self):
        return self.name
