from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'image', 'email', 'first_name', 'last_name', 'bio', 'points', 'password']
        read_only_fields = ['points']
        extra_kwargs = {'password': {'write_only': True}}


class UserReadSerializer(UserSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request', None)

        super().__init__(*args, **kwargs)

        if request and request.query_params.get('nested', None) is not None:
            from courses.serializers import CourseSerializer

            self.fields['added_courses'] = CourseSerializer(read_only=True, many=True, source='get_added_courses')
            self.fields['enrolled_courses'] = CourseSerializer(read_only=True, many=True, source='get_enrolled_courses')


class UserCreateUpdateSerializer(UserSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['confirm_password']

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.pop('confirm_password', None)

        if not password or password != confirm_password:
            raise ValidationError('password and confirm_password must be equal')

        return attrs



