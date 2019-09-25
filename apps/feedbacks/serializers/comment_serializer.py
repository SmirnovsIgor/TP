from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from apps.users.models import Organization
from apps.locations.models import Place
from apps.events.models import Event
from apps.feedbacks.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    topic_type = serializers.SerializerMethodField(read_only=True)
    topic = serializers.SerializerMethodField(read_only=True)
    parent_type = serializers.SerializerMethodField(read_only=True)
    parent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True},
                        'created': {'read_only': True},
                        'updated': {'read_only': True},
                        }

    def get_topic(self, obj=None):
        """
        Method to fill out the topic field in serializer
        """
        return obj.topic_type

    def get_topic_type(self, obj=None):
        """
        Method to fill out the topic type in serializer
        It converts model's number into models name
        """
        a = 1
        return obj.topic.__class__.__name__

    def get_parent(self, obj=None):
        """
        Method to fill out the parent field in serializer
        """
        return obj.parent_type

    def get_parent_type(self, obj=None):
        """
        Method to fill out the parent type in serializer
        It converts model's number into models name
        """
        return obj.parent.__class__.__name__
