from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Course
from .serializers import CourseSerializer


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    categories = [{'db_value': category[0], 'title': category[1]} for category in Course.Categories.choices]
    return Response(categories)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_all_languages(request):
    languages = [{'db_value': language[0], 'title': language[1]} for language in Course.Languages.choices]
    return Response(languages)


class CourseListCreateAPIView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'category']
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get('search', None):
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        data = {}

        for category in Course.Categories.values:
            serializer = CourseSerializer(queryset.filter(category=category), many=True)
            data[category] = serializer.data

        return Response(data)


class CourseReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
