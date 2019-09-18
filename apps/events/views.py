from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.locations.models import Place, Address
from apps.locations.serializers import ShortPlaceSerializer, AddressSerializer
from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.base.filters import AddressFilter, PlaceFilter, DateFilter
from tools.action_based_permission import ActionBasedPermission
from tools.custom_permissions import IsOwnerOrAdmin


class EventFilter(PlaceFilter, AddressFilter, DateFilter):
    organizer = filters.UUIDFilter(field_name="organizer_id")
    is_top = filters.BooleanFilter(field_name="is_top")
    is_hot = filters.BooleanFilter(field_name="is_hot")

    class Meta:
        model = Event
        fields = ["place", "address", "organizer", "date__lte", "date__gte", "is_top", "is_hot"]


class EventViewSet(mixins.CreateModelMixin,
                   viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet which provides `retrieve()`,
    `list()` and `create()` actions
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ['retrieve', 'list'],
        IsAuthenticated: ['create'],
    }
    filter_backends = [filters.DjangoFilterBackend, rest_filters.OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ("created",)
    ordering = ("created",)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
