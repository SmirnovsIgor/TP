from django_filters import rest_framework as filters
from rest_framework import viewsets

from apps.events.models import Event
from apps.events.serializers import EventSerializer


class EventFilter(filters.FilterSet):
    place = filters.UUIDFilter(field_name="place_id")
    address = filters.UUIDFilter(field_name="address_id")
    organizer = filters.UUIDFilter(field_name="organizer_id")
    date__gte = filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateTimeFilter(field_name="date", lookup_expr="lte")
    is_top = filters.BooleanFilter(field_name="is_top")
    is_hot = filters.BooleanFilter(field_name="is_hot")

    class Meta:
        model = Event
        fields = ["place", "address", "organizer", "date__lte", "date__gte", "is_top", "is_hot"]


class EventViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing and retrieving events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.OrderingFilter, filters.DjangoFilterBackend]
    filter_class = EventFilter
    ordering = ("created",)
