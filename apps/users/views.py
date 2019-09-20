from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.subscriptions.models import Subscription
from apps.subscriptions.serializers import SubscriptionSerializer
from tools.action_based_permission import ActionBasedPermission
from apps.base.filters import SubscriptionDateFilter


class SubscriptionFilter(SubscriptionDateFilter):
    class Meta:
        model = Subscription
        fields = ['eventdate__lte', 'eventdate__gte']


class UserDataForStaffViewSet(RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['retrieve', 'subscriptions']
    }

    @action(detail=True, methods=['get'])
    def subscriptions(self, request, pk=None):
        self.filter_backends = [SubscriptionFilter]
        user = self.get_object()
        serializer = SubscriptionSerializer(user.events, many=True)
        return Response(serializer.data)
