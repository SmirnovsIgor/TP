from django.db import models

from apps.base.models.base_model import BaseModel
from apps.locations.models.address import Address


class Place(BaseModel):
    WORKING = 'WORKING'
    TEMPORARILY_CLOSED = 'TEMPORARILY_CLOSED'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (TEMPORARILY_CLOSED, 'Temporarily closed'),
        (WORKING, 'Working'),
        (CLOSED, 'Closed'),
    ]
    name = models.CharField(max_length=75, blank=False, null=False)
    address = models.OneToOneField(Address, on_delete=models.PROTECT)
    photo = models.ImageField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, blank=False, null=False)

