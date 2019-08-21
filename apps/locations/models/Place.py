from django.db import models

from apps.base.models import BaseModel
from apps.locations.models import Address


class Place(BaseModel):
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (ACTIVE, 'Working'),
        (CLOSED, 'Closed'),
    ]
    name = models.CharField(max_length=75, blank=False, null=False)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    photo = models.ImageField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, blank=False, null=False)

    # Required method to set place closed instead of deleting it
