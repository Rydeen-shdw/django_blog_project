from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        if User.objects.filter(email=email).first():
            raise serializers.ValidationError({'email': 'Email is already registered.'})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'This username is already taken.'})

        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class ActivateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()