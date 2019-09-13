from django.db import models

from apps.base.models.base import BaseAbstractModel


class Address(BaseAbstractModel):
    country = models.CharField(max_length=30, blank=False, null=False)
    city = models.CharField(max_length=30, blank=False, null=False)
    street = models.CharField(max_length=30, blank=True, null=True)
    house = models.CharField(max_length=10, blank=True, null=True)
    floor = models.PositiveSmallIntegerField(blank=True, null=True)
    apartments = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return ' '.join([str(item) for item in
                         (self.country, self.city, self.street, self.house, self.floor, self.apartments) if item])
