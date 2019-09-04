from apps.users.models import User
from apps.users.serializers.user_serializer import UserSerializer


class UserSerializerForStaff(UserSerializer):

    class Meta:
        model = User
        fields = ['id', 'is_staff', 'is_active', 'email', 'first_name', 'last_name']
