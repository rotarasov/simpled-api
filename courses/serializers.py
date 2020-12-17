from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Course, Task, Solution
from users.serializers import UserSerializer


User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False,
                                                      many=True)
    is_active = serializers.BooleanField(default=True)

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
                self.fields['participants'] = UserSerializer(many=True)

            else:
                self.fields['creator'] = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_participants(self, value):
        if any(user == self.instance.creator for user in value):
            raise serializers.ValidationError(_('Creator can not be participant of the course.'))

        if len(set(value)) != len(value):
            raise serializers.ValidationError(_('Participants can not ve duplicated in the list'))

        return value

    def update(self, instance, validated_data):
        is_active = validated_data.get('is_active', True)
        make_inactive = not is_active

        if instance.is_active and make_inactive:
            instance.delete_solutions()
            instance.delete_participants()

        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SolutionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Solution
        fields = '__all__'

    def validate(self, attrs):
        text = attrs.get('text', getattr(self.instance, 'text', None))
        file = attrs.get('file', getattr(self.instance, 'file', None))

        if not text and not file:
            raise serializers.ValidationError(_('Either file or text must be sent.'))

        return attrs


class SolutionOwnerDetailSerializer(SolutionSerializer):
    owner = UserSerializer()
