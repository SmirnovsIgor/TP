from django_filters import rest_framework as filters
from rest_framework import viewsets

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
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter
