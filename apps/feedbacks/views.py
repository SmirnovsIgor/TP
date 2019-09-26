import uuid

from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event
from apps.feedbacks.models import Comment, Review
from apps.feedbacks.serializers.comment_serializer import CommentSerializer
from apps.locations.models import Place
from apps.users.models import Organization
from tools.action_based_permission import ActionBasedPermission
from tools.custom_permissions import IsOwnerOrAdmin, IsOwner


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for Comment model, which provides
    `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list'],
        IsAuthenticated: ['create'],
        IsOwner: ['update', 'partial_update'],
        IsOwnerOrAdmin: ['destroy'],
    }

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(status=Comment.DELETED))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data_dict = request.data
        models_mapping = {
            Event.__name__: (Event, ContentType.objects.get_for_model(Event)),
            Organization.__name__: (Organization, ContentType.objects.get_for_model(Organization)),
            Place.__name__: (Place, ContentType.objects.get_for_model(Place)),
            Comment.__name__: (Comment, ContentType.objects.get_for_model(Comment)),
            Review.__name__: (Review, ContentType.objects.get_for_model(Review)),
        }
        self.validate_data(data_dict)
        topic_id, topic_type = self.get_topic_or_parent(data_dict, models_mapping, 'topic')
        parent_id, parent_type = self.get_topic_or_parent(data_dict, models_mapping, 'parent')
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer, created_by=user, topic_type=topic_type,
                                      topic_id=topic_id, parent_type=parent_type, parent_id=parent_id)
        comment_data = serializer_class(comment).data
        headers = self.get_success_headers(comment_data)
        return Response(comment_data, status=status.HTTP_201_CREATED, headers=headers)

    def validate_data(self, data_dict):
        for item in ('topic', 'topic_type', 'parent', 'parent_type'):
            if item not in data_dict:
                raise exceptions.ParseError('Please, transmit topic and parent')

    def get_topic_or_parent(self, data_dict, models_mapping, obj_class):
        obj_from_user = data_dict.pop(obj_class)
        obj_type_from_user = data_dict.pop(f'{obj_class}_type').title()
        obj_model, obj_type = models_mapping.get(obj_type_from_user)
        obj = self.get_created_object(obj_from_user.get('id'), obj_model)
        obj_id = obj.id
        return obj_id, obj_type

    def get_created_object(self, obj_id, cls):
        """Validates ID"""
        try:
            return cls.objects.get(id=uuid.UUID(str(obj_id)))
        except ValueError:
            raise exceptions.ParseError(f'{cls.__name__}\'s ID is not valid')
        except cls.DoesNotExist:
            raise exceptions.NotFound('No such ID in database')

    def perform_create(self, serializer, **kwargs):
        return Comment.objects.create(**kwargs, **serializer.validated_data)

    def perform_destroy(self, instance):
        instance.status = Comment.DELETED
        instance.save()
