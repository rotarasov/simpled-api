from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer


# TODO: add course list and group by categories

@api_view(http_method_names=['GET'])
def get_all_categories(request):
    categories = {
        'categories': [
            {'db_value': category[0], 'human_readable_name': category[1]} for category in Course.Categories.choices
        ]
    }
    return Response(categories)


@api_view(http_method_names=['GET'])
def get_all_languages(request):
    languages = {
        'languages': [
            {'db_value': language[0], 'human_readable_name': language[1]} for language in Course.Languages.choices
        ]
    }
    return Response(languages)


class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

