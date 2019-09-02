from rest_framework.response import Response

from rest_auth.views import UserDetailsView

from apps.users.serializers.user_serializer import UserSerializer


class PersonalData(UserDetailsView):
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        # instance = self.get_object()
        # serializer = UserSerializer(
        #     instance=instance,
        #     data=request.data
        # )
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pass






