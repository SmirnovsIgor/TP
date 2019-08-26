from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.base.models import BaseAbstractModel
from apps.locations.models import Place, Address

from tools.image_funcs import get_posters_path


class Event(BaseAbstractModel):
    """
    Event Model inherited from BaseModel.
    Fields id, created, updated were inherited
    """
    name = models.CharField(max_length=64)
    description = models.TextField()
    poster = models.ImageField(upload_to=get_posters_path, blank=True, null=True)
    organizer_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    organizer_id = models.UUIDField()
    organizer = GenericForeignKey('organizer_type', 'organizer_id')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateTimeField()
    duration = models.DurationField()
    age_rate = models.PositiveSmallIntegerField()
    is_approved = models.BooleanField()
    max_members = models.PositiveIntegerField()
    ratings = models.DecimalField(max_digits=2, decimal_places=1)
    SOON = "SOON"
    SUCCEED = "SUCCEED"
    REJECTED = "REJECTED"
    STATUS_TYPES = (
        (SOON, "soon"),
        (SUCCEED, "succeed"),
        (REJECTED, 'rejected'),
    )
    status = models.CharField(max_length=16, choices=STATUS_TYPES, default=SOON)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not Event.objects.get(organizer_id=self.organizer_id).exists():
            self.organizer = self.organizer.membership.organization if self.organizer.membership else self.organizer
        super().save(self, *args, **kwargs)
