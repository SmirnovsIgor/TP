from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models

from apps.base.models import BaseAbstractModel
from apps.users.models import User


class Comment(BaseAbstractModel):
    OK = 'OK'
    SUSPICIOUS = 'SUSPICIOUS'
    DELETED = 'DELETED'
    STATUS_TYPES = {
        (OK, 'ok'),
        (SUSPICIOUS, 'suspicious'),
        (DELETED, 'deleted')
    }
    topic_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='topic_type')
    topic_id = models.UUIDField(editable=False)
    topic = GenericForeignKey('topic_type', 'topic_id')
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='parent_type')
    parent_id = models.UUIDField(editable=False)
    parent = GenericForeignKey('parent_type', 'parent_id')
    author = models.ForeignKey(User, null=False, blank=False, editable=False,
                               on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=16, choices=STATUS_TYPES, default=OK)
    comments = GenericRelation(
        'feedbacks.Comment',
        content_type_field='parent_type',
        object_id_field='parent_id',
        related_name='comments'
    )

    def __str__(self):
        return f'{self.author.username}: {self.text[:10]+"..." if len(self.text)>10 else self.text}'
