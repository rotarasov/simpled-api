from rest_framework import serializers

from .models import Course
from users.models import User

class CourseSerializer(serializers.ModelSerializer):
    # Uncomment when authorisation is provided
    # creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    creator = serializers.PrimaryKeyRelatedField(read_only=True, default=User.objects.first()) # REMOVE LATER
    participants = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['creator']
