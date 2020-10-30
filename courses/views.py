from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer


# TODO: add course list and group by categories

@api_view(http_method_names=['GET'])
def get_all_categories(request):
    categories = [{'db_value': category[0], 'title': category[1]} for category in Course.Categories.choices]
    return Response(categories)


@api_view(http_method_names=['GET'])
def get_all_languages(request):
    languages = [{'db_value': language[0], 'title': language[1]} for language in Course.Languages.choices]
    return Response(languages)


class CourseListCreateAPIView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {}

        for category in Course.Categories.values:
            serializer = CourseSerializer(queryset.filter(category=category), many=True)
            data[category] = serializer.data

        return Response(data)


class CourseReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

