from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    profile_image = serializers.ImageField(required=False, allow_empty_file=True, allow_null=True)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=30)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=150)
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_lengh=150)
    is_staff = serializers.BooleanField(default=False, allow_null=False)
    is_active = serializers.BooleanField(default=True, allow_null=False)