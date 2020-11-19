from django.urls import reverse
from django.test import TestCase
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Course, Task, Solution
from .serializers import CourseSerializer


User = get_user_model()


class CourseSerializerTestCase(TestCase):
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


class CourseManagementAPITestCase(APITestCase):
    course_list_url = reverse('course-list')
    course_detail_url = reverse('course-detail', kwargs={'pk': 1})
    obtain_token_url = reverse('token-obtain-pair')
    task_list_url = reverse('task-list', kwargs={'pk': 1})
    task_detail_url = reverse('task-detail', kwargs={'course_pk': 1, 'task_pk': 1})

    def setUp(self) -> None:
        user = User.objects.create_user(email='normal@user.com', password='foo',
                                        first_name='first name 1', last_name='last name 1')
        course = Course.objects.create(
            title='Course Title 1',
            category='music',
            language='ru',
            creator=user,
            description='Course description 1'
        )

        self.set_credentials()

    def set_credentials(self):
        response = self.client.post(self.obtain_token_url, data={'email': 'normal@user.com', 'password': 'foo'})
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_course_creation(self):
        data = {'title': 'Course Title 2', 'category': 'math', 'language': 'en', 'description': 'Course description 2',
                'creator': 1}
        response = self.client.post(self.course_list_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(response.data['title'], 'Course Title 2')
        self.assertEqual(response.data['category'], 'math')
        self.assertEqual(response.data['language'], 'en')

    def test_course_read(self):
        response = self.client.get(self.course_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Course Title 1')
        self.assertEqual(response.data['category'], 'music')
        self.assertEqual(response.data['language'], 'ru')

    def test_course_update(self):
        response = self.client.patch(self.course_detail_url, data={'title': 'Course Title 3'},  format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Course Title 3')

    def test_course_delete(self):
        response = self.client.delete(self.course_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class AssessmentManagementAPITestCase(APITestCase):
    obtain_token_url = reverse('token-obtain-pair')
    task_list_url = reverse('task-list', kwargs={'pk': 1})
    task_detail_url = reverse('task-detail', kwargs={'course_pk': 1, 'task_pk': 1})
    solution_list_url = reverse('solution-list', kwargs={'course_pk': 1, 'task_pk': 1})
    solution_detail_url = reverse('solution-detail', kwargs={'course_pk': 1, 'task_pk': 1, 'solution_pk': 1})

    def setUp(self) -> None:
        user = User.objects.create_user(email='normal@user.com', password='foo',
                                        first_name='first name 1', last_name='last name 1')
        course = Course.objects.create(
            title='Course Title 1',
            category='music',
            language='ru',
            creator=user,
            description='Course description 1'
        )

        task1 = Task.objects.create(title='t1', description='d1', deadline='2020-11-20T00:00Z', course=course)
        task2 = Task.objects.create(title='t2', description='d2', deadline='2020-11-20T00:00Z', course=course)

        Solution.objects.create(owner=user, task=task1, text='t1')

        self.set_credentials()

    def set_credentials(self):
        response = self.client.post(self.obtain_token_url, data={'email': 'normal@user.com', 'password': 'foo'})
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_task_create(self):
        data = {'title': 't3', 'description': 'd3', 'deadline': '2020-11-20T00:00Z', 'course': 1}
        response = self.client.post(self.task_list_url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 't3')
        self.assertEqual(response.data['description'], 'd3')
        self.assertEqual(response.data['deadline'], '2020-11-20T00:00:00Z')
        self.assertIsNotNone(response.data['created'])
        self.assertIsNotNone(response.data['last_modified'])

    def test_task_list(self):
        response = self.client.get(self.task_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.filter(course_id=1).count())

    def test_solution_list(self):
        response = self.client.get(self.solution_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Solution.objects.filter(task_id=1).count())
        self.assertTrue(isinstance(response.data[0]['owner'], dict))

    def test_solution_create(self):
        data = {'owner': 1, 'task': 2, 'text': 't2', 'course': 1}
        response = self.client.post(self.solution_list_url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], 1)
        self.assertEqual(response.data['task'], 2)
        self.assertEqual(response.data['text'], 't2')

        data['text'] = 't3'
        response = self.client.post(self.solution_list_url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_solution_read(self):
        response = self.client.get(self.solution_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 't1')
