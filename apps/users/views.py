from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from django.shortcuts import get_object_or_404

from apps.events.models import Event
from apps.events.serializers import EventSerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserDataForStaffView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User does not exist")
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


class UserEventsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = request.user.events
        serializer = EventSerializer(response, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=kwargs.get('event_id'))
        serializer = EventSerializer(event)
        return Response(serializer.data, status=HTTP_200_OK)
