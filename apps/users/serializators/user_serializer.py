from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    profile_image = serializers.ImageField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=150)
    username = serializers.CharField(required=True, max_lengh=150)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
