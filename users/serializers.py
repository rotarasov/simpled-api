from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'image', 'email', 'first_name', 'last_name', 'bio', 'points']
        read_only_fields = ['points']


class UserReadSerializer(UserSerializer):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request', None)

        super().__init__(*args, **kwargs)

        if request and request.query_params.get('nested', None) is not None:
            from courses.serializers import CourseSerializer

            self.fields['added_courses'] = CourseSerializer(read_only=True, many=True, source='get_added_courses')
            self.fields['enrolled_courses'] = CourseSerializer(read_only=True, many=True, source='get_enrolled_courses')


class UserCreateSerializer(UserSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.pop('confirm_password', None)

        if not password or password != confirm_password:
            raise ValidationError(_('password and confirm_password must be equal'))

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context.get('request').user

        if not user.check_password(value):
            raise ValidationError(_('Wrong password'))

        return value

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')

        if old_password == new_password:
            raise ValidationError(_('Passwords can not be equal'))

        return attrs

    def save(self, **kwargs):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data
