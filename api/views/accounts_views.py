from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from api.serializers.accounts_serializers import UserCreateSerializer, ActivateUserSerializer
from api.utils import send_activation_api_email
from config import settings

from accounts import models
from accounts.models import ActivateToken

User = get_user_model()


class UserCreateAPIView(APIView):
    def post(self, request: Request) -> Response:
        create_serializer = UserCreateSerializer(data=request.data)
        if create_serializer.is_valid():
            user = create_serializer.save()
            user_token = ActivateToken.objects.create(user=user)
            send_activation_api_email(user, user_token, settings.EMAIL_HOST_USER)
            return Response({'message': 'User created successfully. Activation email sent.'},
                                status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserAPIView(APIView):
    def post(self, request: Request) -> Response:
        activate_serializer = ActivateUserSerializer(data=request.data)
        if activate_serializer.is_valid():
            email = activate_serializer.validated_data['email']
            token = activate_serializer.validated_data['token']

            user = get_object_or_404(User, email=email)
            if user.is_active:
                return Response({'message': 'User is already activated.'})

            activate_token = get_object_or_404(ActivateToken, user=user, token=token)

            if activate_token.verify_token():
                user.is_active = True
                activate_token.delete()
                user.save()

            return Response({'detail': 'User activated successfully.'}, status=status.HTTP_200_OK)
        return Response(activate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

