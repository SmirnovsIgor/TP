import uuid

from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status, exceptions, filters as rest_filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.models import User
from apps.locations.models import Place, Address
from apps.locations.serializers import AddressSerializer

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
        address = None

        if 'place' in data_dict:
            place = data_dict.pop('place')
        if 'address' in data_dict:
            address = data_dict.pop('address')

        # ------------------------refactoring-------------------------------------------
        if isinstance(place, (dict, str)):
            mapping = {
                dict: lambda: self.get_created_object(place.get('id'), Place),
                str: lambda: self.get_created_object(place, Place),
            }
            place = mapping.get(type(place))()
            address = self.get_created_object(place.address_id, Address)
        elif isinstance(address, dict):
            if address.get('id'):
                address = self.get_created_object(address.get('id'), Address)
            else:
                address_serializer = AddressSerializer(data=address)
                if address_serializer.is_valid():
                    address = Address.objects.create(**address_serializer.validated_data)
                else:
                    raise exceptions.ParseError('Address data is invalid')
        elif isinstance(address, str):
            address = self.get_created_object(address, Address)
        else:
            raise exceptions.ParseError('Please, transmit address or place as dict or str')
        # if place is None:
        #     if address is None:
        #         raise exceptions.ParseError('Please, transmit address or place data')
        #     elif isinstance(address, dict):
        #         if address.get('id'):
        #             address = self.get_created_object(address.get('id'), Address)
        #         else:
        #             address_serializer = AddressSerializer(data=address)
        #             if address_serializer.is_valid():
        #                 address = Address.objects.create(**address_serializer.validated_data)
        #             else:
        #                 raise exceptions.ParseError('Address invalid')
        #     elif isinstance(address, str):
        #         address = self.get_created_object(address, Address)
        #     else:
        #         raise exceptions.ParseError('Address field is filled out improperly')
        # elif isinstance(place, dict):
        #     place = self.get_created_object(place.get('id'), Place)
        #     address = self.get_created_object(place.address_id, Address)
        # elif isinstance(place, str):
        #     place = self.get_created_object(place, Place)
        #     address = self.get_created_object(place.address_id, Address)
        # else:
        #     raise exceptions.ParseError('Please, transmit address or place data')
        # ------------------------refactoring-------------------------------------------

        organizer, data_dict = self.choose_event_organizer(user=user, **data_dict)
        data_dict = self.set_defaults(**data_dict)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data_dict)
        serializer.is_valid(raise_exception=True)
        event = self.perform_create(serializer, address=address, place=place, organizer=organizer)
        event_data = serializer_class(event).data
        headers = self.get_success_headers(event_data)
        return Response(event_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_created_object(self, obj_id, cls):
        """Validates ID"""
        try:
            return cls.objects.get(id=uuid.UUID(str(obj_id)))
        except ValueError:
            raise exceptions.ParseError(f'{cls.__name__}\'s ID is not valid')
        except cls.DoesNotExist:
            raise exceptions.NotFound('No such ID in database')

    def choose_event_organizer(self, user, **data_dict):
        """Checks if a user is a member of any organization"""
        try:
            organizer = user.membership.organization
        except User.membership.RelatedObjectDoesNotExist:
            organizer = user
        organizer_id, organizer_type = (
            organizer.id,
            ContentType.objects.get_for_model(organizer.__class__)
        )
        data_dict.update(dict(organizer_id=organizer_id, organizer_type=organizer_type))
        return organizer, data_dict

    def set_defaults(self, **data_dict):
        """Set defaults to important fields"""
        defaults = {
            'is_top': False,
            'is_hot': False,
            'is_approved': False,
            'status': Event.SOON,
        }
        data_dict.update(defaults)
        return data_dict

    def perform_create(self, serializer, **kwargs):
        return Event.objects.create(**kwargs, **serializer.validated_data)
