import os

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from apps.base import models as custmodels

# Create your models here.


def get_image_path(instance: object, filename: str):
    """
    Gets path for event's poster '/static/posters/{event_id}/{filename}
    """
    return os.path.join('posters', instance.id, filename)


class EventModel(custmodels.BaseModel):
    """
    Event Model inherited from BaseModel.
    Fields id, created, updated were inherited
    """
    name = models.CharField(max_length=64)
    description = models.TextField()
    poster = models.ImageField(upload_to=get_image_path,
                               null=True,
                               blank=True)
    organizer = models.ForeignKey('User',
                                  on_delete=models.CASCADE)
    place = models.ForeignKey('Place',
                              null=True,
                              on_delete=models.CASCADE)
    address = models.ForeignKey('Address',
                                on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration = models.DurationField()
    age_rate = models.PositiveSmallIntegerField()
    is_approved = models.BooleanField()
    max_members = models.PositiveIntegerField()
    ratings = models.DecimalField(max_digits=2,
                                  decimal_places=1)

    SOON = "SOON"
    SUCCEED = "SUCCEED"
    REJECTED = "REJECTED"
    STATUS_TYPES = (
        (SOON, "soon"),
        (SUCCEED, "succeed"),
        (REJECTED, 'rejected'),
    )
    status = models.CharField(max_length=1,
                              choices=STATUS_TYPES,
                              default=SOON)
