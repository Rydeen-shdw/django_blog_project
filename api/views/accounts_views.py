from django.contrib.auth import get_user_model
from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from api.serializers.accounts_serializers import UserCreateSerializer
from api.utils import send_activation_api_email
from config import settings

from accounts import models
from accounts.models import ActivateToken

User = get_user_model()


class UserCreatePIView(APIView):
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
    def get(self, request, token, *args, **kwargs):
        try:
            user_token = models.ActivateToken.objects.get(token=token)
            user = user_token.user
            user.is_active = True
            user.save()
            user_token.delete()
            return Response({'message': 'User activated successfully.'}, status=status.HTTP_200_OK)
        except models.ActivateToken.DoesNotExist:
            return Response({'message': 'Invalid activation token.'}, status=status.HTTP_400_BAD_REQUEST)


