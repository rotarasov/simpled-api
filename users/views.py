from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

from .serializers import UserSerializer


User = get_user_model()

# TODO: create post delete hook to delete picture from cloudinary

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
