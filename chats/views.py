from rest_framework.generics import ListAPIView, get_object_or_404

from courses.models import Course
from .serializers import MessageSerializer
from .models import Message


class MessageListAPIView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['pk'])
        return Message.objects.filter(course=course)
