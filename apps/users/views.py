from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.users.models import User, Organization
from apps.users.serializers import UserSerializer, ShortOrganizationSerializer
from apps.users.serializers.organization_serializer import (OrganizationWithEventsSerializer,
                                                            DetailedOrganizationWithMembersSerializer)


class UserDataForStaffView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, uuid):
        user = get_object_or_404(User, id=uuid)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)


class OrganizationsView(APIView):
    def get(self, request):
        organizations = self.get_queryset()
        serializer = ShortOrganizationSerializer(organizations, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()


class DetailsWithAllEventsOrganizationView(APIView):
    def get(self, request, uuid):
        organization = get_object_or_404(self.get_queryset(), id=uuid)
        serializer = OrganizationWithEventsSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()


class DetailedOrganizationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, uuid):
        organization = get_object_or_404(self.get_queryset(), id=uuid)
        serializer = DetailedOrganizationWithMembersSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()
