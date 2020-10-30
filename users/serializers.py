from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'image', 'email', 'first_name', 'last_name', 'bio', 'points']
        read_only_fields = ['points']

    def __init__(self, *args, **kwargs):
        request = kwargs.get('context', {}).get('request')

        super().__init__(*args, **kwargs)

        if request and request.query_params.get('nested', None) is not None:
            from courses.serializers import CourseSerializer

            self.fields['added_courses'] = CourseSerializer(many=True, source='get_added_courses')
            self.fields['enrolled_courses'] = CourseSerializer(many=True, source='get_enrolled_courses')