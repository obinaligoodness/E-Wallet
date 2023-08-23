from djoser.serializers import UserCreateSerializer


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['email', 'phone', 'password', 'first_name', 'last_name','username']
