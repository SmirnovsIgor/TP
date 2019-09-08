import uuid

from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from apps.events.models import Event
from apps.events.serializers import EventSerializer


class EventFilter(filters.FilterSet):

    class Meta:
        model = Event
        fields = {
            "date": ["gte", "lte"],
            "is_hot": ["exact"],
            "is_top": ["exact"],
        }


class EventViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing and retrieving events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # filter_backends = [filters.DjangoFilterBackend]
    # the problem is how to combine filterset_class and filterset_fields
    # filterset_class = EventFilter
    filterset_fields = ['place', 'address', 'organizer_id', 'is_hot', 'is_top']
    ordering_fields = ['created']

    # def get_queryset(self):
    #     super().get_queryset()
    #     place = self.request.query_params.get('place', None)
    #     ordered = self.request.query_params.get('ordered', None)
    #     if place is not None:
    #         if place == 'null':
    #             self.queryset = self.queryset.filter(place__isnull=True)
    #         else:
    #             try:
    #                 uuid.UUID(place)
    #             except ValueError:
    #                 return Response(status=status.HTTP_400_BAD_REQUEST)
    #             self.queryset = self.queryset.filter(place=place)
    #     if ordered in ['desc', 'asc']:
    #         self.queryset = self.queryset.order_by('created') if ordered == 'asc' else self.queryset.order_by('-created')
    #     return self.queryset
