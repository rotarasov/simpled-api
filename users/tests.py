from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from cloudinary import api
from cloudinary.models import CloudinaryResource

class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo',
                                        first_name='first name 1', last_name='last name 1')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.first_name, 'first name 1')
        self.assertEqual(user.last_name, 'last name 1')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo",
                                     first_name='first name 1', last_name='last name 1')
        with self.assertRaises(TypeError):
            User.objects.create_user(email='normal@user.com', password="foo")
        with self.assertRaises(TypeError):
            User.objects.create_user(email='normal@user.com', password="foo", first_name='')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo',
                                                   first_name='first name 1', last_name='last name 1')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.first_name, 'first name 1')
        self.assertEqual(admin_user.last_name, 'last name 1')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo',
                first_name='first name 1', last_name='last name 1',
                is_superuser=False)

    def test_user_image(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo',
                                        first_name='first name 1', last_name='last name 1')
        result = CloudinaryResource(api.resource('profile_pics/default'))
        self.assertEqual(user.image.url, result.get_prep_value())



class UsersAPITestCase(APITestCase):

    def setUp(self) -> None:
        User = get_user_model()
        User.objects.create_user(email='u1@gmail.com', password='p1',
                                 first_name='first_name1', last_name='last_name1')
        User.objects.create_user(email='u2@gmail.com', password='p2',
                                 first_name='first_name2', last_name='last_name2')

        self.users_count = User.objects.count()

    def test_user_creation(self):
        User = get_user_model()
        data = {'email': 'u3@gmail.com', 'password':'p3', 'first_name': 'first_name3', 'last_name': 'last_name3'}
        url = reverse('user-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.users_count + 1)

    def test_user_read(self):
        User = get_user_model()
        user = User.objects.get(pk=1)
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertIsNotNone(response.data['image'])

    def test_user_update(self):
        User = get_user_model()
        url = reverse('user-detail', kwargs={'pk': 1})
        data = {'email': 'u2@gmail.com'}

        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['email'] = 'u3@gmail.com'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'u3@gmail.com')

        data = {'pk': 1, 'email': 'u4@gmail.com', 'password': 'p4',
                'first_name': 'first_name4', 'last_name': 'last_name4'}
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'u4@gmail.com')
        self.assertEqual(response.data['first_name'], 'first_name4')

    def test_user_delete(self):
        User = get_user_model()
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), self.users_count - 1)




