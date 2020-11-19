from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserSerializer,
    UserReadSerializer,
    UserCreateSerializer,
    CustomTokenObtainPairSerializer,
    UserUpdatePasswordSerializer
)


User = get_user_model()


@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated])
def update_user_password(request, *args, **kwargs):
    serializer = UserUpdatePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user_serializer = UserSerializer(serializer.save())
    return Response(user_serializer.data)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserReadSerializer
        return UserSerializer


class CustomTokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
