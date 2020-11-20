from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Course, Task, Solution
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


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SolutionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Solution
        fields = '__all__'
        extra_kwargs = {'task': {'read_only': True}}

    def validate(self, attrs):
        text = attrs.get('text', None)
        file = attrs.get('file', None)

        if not text and not file:
            raise serializers.ValidationError(_('Either file or text must be sent'))

        return attrs


class SolutionOwnerDetailSerializer(SolutionSerializer):
    owner = UserSerializer()
