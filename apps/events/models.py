import os

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.base import models as custmodels


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
                               blank=True,
                               null=True)
    organizer_type = models.ForeignKey(ContentType,
                                       on_delete=models.CASCADE)
    organizer_id = models.UUIDField()
    organizer = GenericForeignKey('content_type', 'organizer_id')
    location_type = models.ForeignKey(ContentType,
                                      on_delete=models.CASCADE)
    location_id = models.UUIDField()
    location = GenericForeignKey('location_type', 'location_id')
    # place = models.ForeignKey('Place',
    #                           on_delete=models.CASCADE,
    #                           null=True)
    # address = models.ForeignKey('Address',
    #                             on_delete=models.CASCADE)
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

    def save(self, *args, **kwargs):
        user = User.objects.get(id=self.organizer_id)
        if user.objects.get(organization__id) is not None:
            organization = user.objects.get(organization__id)
            self.organizer = GenericForeignKey(organization)
        super().save(self, *args, **kwargs)
