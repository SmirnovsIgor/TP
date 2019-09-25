import uuid

from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from tools.custom_permissions import IsSubscriberOrAdmin

from apps.events.models import Event
from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer
from tools.action_based_permission import ActionBasedPermission


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['list', 'update', 'partial_update'],
        IsAuthenticated: ['create', 'destroy'],
        IsSubscriberOrAdmin: ['retrieve'],
    }

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        subscribed_event_id = self.get_event_id(data)
        if subscribed_event_id:
            subscribed_event = self.get_obj_by_id(subscribed_event_id, Event)
        else:
            exceptions.ParseError('Please, transmit event as dict or str.')
        if subscribed_event.is_available_for_subscription:
            response = self.create_subscription(user, subscribed_event)
        else:
            exceptions.PermissionDenied('Too late to subscribe.')
        return response

    def list(self, request, *args, **kwargs):
        return Subscription.objects.all().filter(status__in=[Subscription.STATUS_REJECTED,
                                                             Subscription.STATUS_ACTIVE,
                                                             Subscription.STATUS_UNTRACKED])

    def retrieve(self, request, *args, **kwargs):
        if self.get_object().status == Subscription.STATUS_CANCELLED:
            exceptions.NotFound('No subscription found.')

    def destroy(self, request, *args, **kwargs):


    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        approved_subscription = self.get_obj_by_id(pk, Subscription)
        if request.user == approved_subscription.user:
            if approved_subscription.event.is_available_for_subscription:
                response = self.approve_subscription(approved_subscription)
            else:
                exceptions.PermissionDenied('Too late to subscribe.')
        else:
            exceptions.PermissionDenied('You could approve only your own subscriptions.')
        return response

    def get_event_id(self, data):
        event = None
        if 'event' in data:
            event = data.pop('event')
        else:
            exceptions.ParseError('You must transmit event id.')

        if isinstance(event, (str, dict)):
            return event if isinstance(event, str) else event.get('id')
        else:
            exceptions.ParseError('Please, transmit event as dict or str.')

    def get_obj_by_id(self, obj_id, cls):
        try:
            return cls.objects.get(id=uuid.UUID(str(obj_id)))
        except ValueError:
            raise exceptions.ParseError(f'{cls.__name__}\'s ID is not valid.')
        except cls.DoesNotExist:
            raise exceptions.NotFound('No such ID in database.')

    def create_subscription(self, user, event):
        duplicate = Subscription.objects.all().filter(user=user, event=event)
        if not duplicate:
            subscription = Subscription.objects.create(user=user, event=event)
            subscription_data = SubscriptionSerializer(subscription).data
            return Response(subscription_data, status=status.HTTP_201_CREATED)
        else:
            if duplicate.status in (
                    Subscription.STATUS_ACTIVE,
                    Subscription.STATUS_UNTRACKED,
                    Subscription.STATUS_REJECTED,
                    ):
                return Response(status=status.HTTP_409_CONFLICT)
            elif duplicate.status == Subscription.STATUS_CANCELLED:
                duplicate.set_status(Subscription.STATUS_UNTRACKED)
                duplicate_data = SubscriptionSerializer(duplicate).data
                return Response(duplicate_data, status=status.HTTP_201_CREATED)

    def approve_subscription(self, subscription):
        if subscription.status == Subscription.STATUS_UNTRACKED:
            subscription.set_status(Subscription.STATUS_ACTIVE)
            subscription_data = SubscriptionSerializer(subscription).data
            return Response(subscription_data, status=status.HTTP_200_OK)
        elif subscription.status == Subscription.STATUS_ACTIVE:
            return Response(status=status.HTTP_409_CONFLICT)
        elif subscription.status == Subscription.STATUS_REJECTED:
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif subscription.status == Subscription.STATUS_CANCELLED:
            return Response(status=status.HTTP_400_BAD_REQUEST)
