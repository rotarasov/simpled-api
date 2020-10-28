from django.test import TestCase
from django.http.request import HttpRequest
from rest_framework.request import Request

from .models import Course
from .serializers import CourseSerializer
from users.models import User


class CourseManagementTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(email='normal@user.com', password='foo',
                                        first_name='first name 1', last_name='last name 1')
        Course.objects.create(
            title='Course Title 1',
            category='programming',
            language='ru',
            creator=user,
            description='Course description 1'
        )

    def test_course_serializer(self):
        user = User.objects.get(pk=1)
        course = Course.objects.get(pk=1)
        serializer = CourseSerializer(course)
        self.assertEqual(serializer.data['title'], 'Course Title 1')
        self.assertEqual(serializer.data['creator'], user.id)

    def test_course_serializer_relations(self):
        user = User.objects.get(pk=1)
        request = Request(HttpRequest())
        request.user = user
        data = {'title': 'Course Title 2', 'category': 'programming', 'language': 'en',
                'description': 'Course description 2'}
        serializer = CourseSerializer(data=data, context= {'request': request})
        serializer.is_valid(raise_exception=True)
        course = serializer.save(creator=user)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(course.creator, user)
