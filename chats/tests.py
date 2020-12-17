from datetime import date

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator

from courses.models import Course
from simpled.asgi import application

User = get_user_model()


class WebsocketTestCase(TestCase):
    obtain_token_url = reverse('token-obtain-pair')
    websocket_path = 'chat/1/'

    def setUp(self) -> None:
        self.creator = User.objects.create(email='c1@example.com', password='c1', first_name='User',
                                           last_name='Test1')
        self.user = User.objects.create(email='u1@example.com', password='u1', first_name='User',
                                        last_name='Test2')
        self.course = Course.objects.create(creator=self.creator, title='t1', description='d1', category='music',
                                            language='eu', start_date=date(2020, 12, 20))
        self.course.participants.add(1, 2)

    async def test_messages(self):
        communicator = WebsocketCommunicator(application, self.websocket_path)
        await communicator.connect()
