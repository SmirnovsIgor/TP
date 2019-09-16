from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action

from apps.users.models import User
from apps.users.serializers import UserSerializer
from tools.action_based_permission import ActionBasedPermission


class UserDataForStaffViewSet(RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['retrieve']
    }
