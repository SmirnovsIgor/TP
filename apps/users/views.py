from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from apps.users.models import User
from apps.users.serializers import UserSerializerForStaff


class UserDataForStaffView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, uuid):
        try:
            user = User.objects.get(id=uuid)
            serializer = UserSerializerForStaff(user)
            return Response(serializer.data, status=HTTP_200_OK)
        except User.DoesNotExist:
            return Response('User Not Found', status=HTTP_404_NOT_FOUND)