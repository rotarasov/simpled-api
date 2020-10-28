from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Course
from .serializers import CourseSerializer


class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

