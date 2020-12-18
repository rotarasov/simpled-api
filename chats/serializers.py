from django.contrib.auth import get_user_model
from rest_framework import serializers

from chats.models import Message
from users.serializers import UserSerializer


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'
