import uuid

from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status, exceptions, filters as rest_filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.models import User, Organization, MembersList
from apps.locations.models import Place, Address
from apps.locations.serializers import ShortPlaceSerializer, AddressSerializer

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.base.filters import AddressFilter, PlaceFilter, DateFilter
from tools.action_based_permission import ActionBasedPermission


class EventFilter(PlaceFilter, AddressFilter, DateFilter):
    organizer = filters.UUIDFilter(field_name='organizer_id')
    is_top = filters.BooleanFilter(field_name='is_top')
    is_hot = filters.BooleanFilter(field_name='is_hot')

    class Meta:
        model = Event
        fields = ['place', 'address', 'organizer', 'date__lte', 'date__gte', 'is_top', 'is_hot']


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
        user = request.user
        data_dict = request.data
        place = None
        if 'place' in data_dict:
            place = data_dict.pop('place')
            if place is None:
                pass
            elif place.get('id'):
                place = self.get_created_object(place.get('id'), Place)
                address = self.get_created_object(place.address__id, Address)
                place_serializer = ShortPlaceSerializer(data=place)
                place_serializer.is_valid(raise_exception=True)
                address_serializer = AddressSerializer(data=address)
                address_serializer.is_valid(raise_exception=True)
                # data_dict['place'] = place_serializer
                # data_dict['address'] = address_serializer
            else:
                raise exceptions.ParseError('Wrong place data: send place id or nothing')
        if 'address' in data_dict and place is None:
            address = data_dict.pop('address')
            if address.get('id'):
                address = self.get_created_object(address.get('id'), Address)
                # data_dict['address'] = address
            elif address:
                # address creation
                address_serializer = AddressSerializer(data=address)
                if address_serializer.is_valid():
                    address = Address.objects.create(**address_serializer.validated_data)
                else:
                    raise exceptions.ParseError('Address invalid')
            else:
                raise exceptions.ParseError('Address field is filled out improperly')
        else:
            raise exceptions.ParseError('Please, transmit address or place data')
        # -----------check if user has a membership in organization --------------
        try:
            organizer = user.membership
            organizer_id = organizer.id
            organizer_type = ContentType.objects.get_for_model(Organization)
        except User.membership.RelatedObjectDoesNotExist:
            organizer = user
            organizer_id = user.id
            organizer_type = ContentType.objects.get_for_model(User)
        finally:
            data_dict['organizer_id'] = organizer_id
            data_dict['organizer_type'] = organizer_type
            data_dict['organizer_type_id'] = organizer_type.id
        # ------------------------------------------------------------------------
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        data_dict['address'] = address
        data_dict['place'] = place
        data_dict['organizer'] = organizer
        data_dict
        Event.objects.create(**data_dict)
        return Response(status=status.HTTP_201_CREATED)
        # event = self.perform_create(serializer, address=address, place=place)
        # event_data = serializer_class(event).data
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_created_object(self, obj_id, cls):
        try:
            return cls.objects.get(id=uuid.UUID(obj_id))
        except ValueError:
            raise exceptions.ParseError('')
        except cls.DoesNotExist:
            raise exceptions.NotFound('')

    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)


"""
from apps.events.views import User, Event
User.objects.filter(membership__isnull=True)
"""