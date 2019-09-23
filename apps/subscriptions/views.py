from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer
from tools.action_based_permission import ActionBasedPermission


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['list'],
    }
