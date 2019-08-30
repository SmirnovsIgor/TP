from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models import User


class UserPage(APIView):
    """View to return details of given user.

    Is accessible only for the user themselves, and for staff members.
    """
    def get(self, request, id):
        user = request.user
        if user.is_staff or user.id == id:
            return Response(user.username, status=200)
        else:
            return Response(status=403)

    def get_queryset(self):
        return User.objects.all()



