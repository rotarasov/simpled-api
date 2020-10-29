from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course
from .serializers import CourseSerializer


# TODO: add course list

@api_view(http_method_names=['GET'])
def get_all_categories(request):
    categories = {
        'categories': [
            {'db value': category[0], 'human-readable name': category[1]} for category in Course.Categories.choices
        ]
    }
    return Response(categories)


@api_view(http_method_names=['GET'])
def get_all_languages(request):
    languages = {
        'languages': [
            {'db value': language[0], 'human-readable name': language[1]} for language in Course.Languages.choices
        ]
    }
    return Response(languages)


class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

