from smtplib import SMTPException

from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserSerializer,
    UserReadSerializer,
    UserCreateSerializer,
    CustomTokenObtainPairSerializer,
    UserUpdatePasswordSerializer,
    UserForVideoChatSerializer)
from .services import get_users_for_video_chat_display, notify_users

User = get_user_model()


@api_view(http_method_names=['PUT'])
def update_user_password(request, *args, **kwargs):
    serializer = UserUpdatePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user_serializer = UserSerializer(serializer.save())
    return Response(user_serializer.data)


@api_view(http_method_names=['GET'])
def get_all_user_video_chat_profiles(request, *args, **kwargs):
    users = get_users_for_video_chat_display()
    serializer = UserForVideoChatSerializer(users, many=True)
    return Response(serializer.data)


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class UserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserReadSerializer
        return UserSerializer


class CustomTokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class NotifyUsersAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            notify_users(request.data['users'], request.data['subject'], request.data['message'])
        except SMTPException:
            raise Http404
        return Response(status=status.HTTP_204_NO_CONTENT)
