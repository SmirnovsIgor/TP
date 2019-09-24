from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from tools.image_funcs import get_image_path
from apps.base.models.base import BaseAbstractModel
from apps.locations.models import Address


class Place(BaseAbstractModel):
    STATUS_WORKING = 'WORKING'
    STATUS_TEMPORARILY_CLOSED = 'TEMPORARILY_CLOSED'
    STATUS_CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (STATUS_TEMPORARILY_CLOSED, 'Temporarily closed'),
        (STATUS_WORKING, 'Working'),
        (STATUS_CLOSED, 'Closed'),
    ]
    name = models.CharField(max_length=75, blank=False, null=False)
    address = models.OneToOneField(Address, related_name='place', on_delete=models.PROTECT)
    photo = models.ImageField(upload_to=get_image_path, blank=False, null=False, default='static/Place/base_image.png')
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=18, choices=STATUS_CHOICES, blank=False, null=False, default=STATUS_WORKING)
    comments = GenericRelation(
        'feedbacks.Comment',
        content_type_field='parent_type',
        object_id_field='parent_object_id',
        related_name='comments'
    )
    topic_comments = GenericRelation(
        'feedbacks.Comment',
        content_type_field='topic_type',
        object_id_field='topic_object_id',
        related_name='topic_comments'
    )

    def __str__(self):
        return self.name
