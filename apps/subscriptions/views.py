from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from tools.custom_permissions import IsSubscriberOrAdmin

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

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        subscription = self.get_object()
        subscription.approve()
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
