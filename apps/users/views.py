from rest_framework.exceptions import NotFound
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
        try:
            user = User.objects.get(id=uuid)
        except User.DoesNotExist:
            raise NotFound("User does not exist")
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
        organization = self.get_queryset().get(id=uuid)
        serializer = OrganizationWithEventsSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()


class DetailedOrganizationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request, uuid):
        organization = self.get_queryset().get(id=uuid)
        serializer = DetailedOrganizationWithMembersSerializer(organization)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_queryset(self):
        return Organization.objects.all()
