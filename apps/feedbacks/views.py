from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status, exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


from apps.users.models import Organization
from apps.locations.models import Place
from apps.events.models import Event
from apps.feedbacks.models import Comment, Review
from apps.feedbacks.serializers.comment_serializer import CommentSerializer
from tools.action_based_permission import ActionBasedPermission


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
    }

    def create(self, request, *args, **kwargs):
        user = request.user
        data_dict = request.data
        topic = topic_type = parent = parent_type = None
        models_mapping = {
            'Event': Event,
            'Organization': Organization,
            'Place': Place,
            'Comment': Comment,
            'Review': Review,
        }
        content_type_models_mapping = {
            'Event': ContentType.objects.get_for_model(Event),
            'Organization': ContentType.objects.get_for_model(Organization),
            'Place': ContentType.objects.get_for_model(Place),
            'Comment': ContentType.objects.get_for_model(Comment),
            'Review': ContentType.objects.get_for_model(Review),
        }

        for item in ('topic', 'topic_type', 'parent', 'parent_type'):
            if item not in data_dict:
                raise exceptions.ParseError('Please, transmit topic and parent')
        topic = data_dict.pop('topic')
        topic_type = data_dict.get('topic_type').title()
        topic_model = models_mapping.get(topic_type)
        topic = topic_model.objects.get(id=topic.get('id'))
        topic_type = content_type_models_mapping.get(topic_type)
        parent = data_dict.pop('parent')
        parent_type = data_dict.get('parent_type').title()
        parent_model = models_mapping.get(parent_type)
        parent = parent_model.objects.get(id=parent.get('id'))
        parent_type = content_type_models_mapping.get(parent_type)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer, author=user, topic_type=topic_type, topic_id=topic, topic=topic,
                                      parent_type=parent_type, parent_id=parent, parent=parent)
        comment_data = serializer_class(comment).data
        headers = self.get_success_headers(comment_data)
        return Response(comment_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, **kwargs):
        return Comment.objects.create(**kwargs, **serializer.validated_data)
