from rest_framework import viewsets

from apps.events.models import Event
from apps.events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing and retrieving events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
