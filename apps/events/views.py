import uuid

from datetime import datetime
from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.events.models import Event
from apps.events.serializers import EventSerializer


@permission_classes((AllowAny,))
class EventList(generics.ListAPIView):
    """
    List of all events
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        date__lte = self.request.query_params.get('date__lte', None)
        date__gte = self.request.query_params.get('date__gte', None)
        place = self.request.query_params.get('place', None)
        is_hot = self.request.query_params.get('is_hot', None)
        is_top = self.request.query_params.get('is_top', None)
        ordered = self.request.query_params.get('ordered', None)
        if date__lte is not None:
            date__lte = datetime.strptime(date__lte, '%Y-%m-%dT%H:%M:%S.%fZ')
            queryset = queryset.filter(date__lte=date__lte)
        if date__gte is not None:
            date__gte = datetime.strptime(date__gte, '%Y-%m-%dT%H:%M:%S.%fZ')
            queryset = queryset.filter(date__gte=date__gte)
        if place is not None:
            if place == 'null':
                queryset = queryset.filter(place__isnull=True)
            else:
                try:
                    uuid.UUID(place)
                except ValueError:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                queryset = queryset.filter(place=place)
        if is_hot is not None:
            queryset = queryset.filter(is_hot=is_hot)
        if is_top is not None:
            queryset = queryset.filter(is_top=is_top)
        if ordered is not None:
            if ordered == 'created':
                queryset = queryset.order_by('created')
            elif ordered == '-created':
                queryset = queryset.order_by('-created')
        return queryset


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
