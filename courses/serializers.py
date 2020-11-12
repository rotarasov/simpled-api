from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Course
from users.serializers import UserSerializer


User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)

        if not request:
            return

        method = request.method
        if method == 'GET':
            if request.query_params.get('nested', None) is not None:
                self.fields['creator'] = UserSerializer()

            else:
                self.fields['creator'] = serializers.PrimaryKeyRelatedField(read_only=True)




