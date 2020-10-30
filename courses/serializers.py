from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Course
from users.serializers import UserSerializer


User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    # Uncomment when authorisation is provided
    # creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)

        if request and request.method == 'GET':
            self.fields['creator'] = UserSerializer()



