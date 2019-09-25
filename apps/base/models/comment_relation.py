from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class CommentAbstractRelationModel(models.Model):
    comments = GenericRelation(
        'feedbacks.Comment',
        content_type_field='parent_type',
        object_id_field='parent_id',
        related_name='comments'
    )

    class Meta:
        abstract = True


class TopicAbstractRelationModel(models.Model):
    topic_comments = GenericRelation(
        'feedbacks.Comment',
        content_type_field='topic_type',
        object_id_field='topic_id',
        related_name='topic_comments'
    )

    class Meta:
        abstract = True
