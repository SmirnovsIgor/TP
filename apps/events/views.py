from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from apps.events.models import Event
from apps.events.serializers import EventSerializer


@permission_classes((AllowAny,))
class EventList(APIView):
    """
    List of all events
    """
    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class EventDetail(APIView):
    """
    Retrieve all details of any event
    """
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        event = self.get_object(id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
