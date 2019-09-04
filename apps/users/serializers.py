from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['profile_image', 'email', 'first_name', 'last_name', 'username', 'date_of_birth']


class UserSerializerForStaff(UserSerializer):

    class Meta:
        model = User
        fields = ['id', 'is_staff', 'is_active', 'email', 'first_name', 'last_name', 'date_of_birth']


class OrganizationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=150, allow_blank=False, allow_null=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    profile_image = serializers.ImageField(allow_empty_file=True, allow_null=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    approved = serializers.BooleanField(default=False)
    date_of_birth = serializers.DateField('date of birth', allow_null=True)
