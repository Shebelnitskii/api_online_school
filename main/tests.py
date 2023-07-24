from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Course, Lesson, Subscription


# Create your tests here.

class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """ Тестирование создание урока """
        data = {
            "name": "Test",
            "description": "test"
        }

        course = Course.objects.create(
            name="Test course",
            description="Test course"
        )

        data["course"] = course.id

        response = self.client.post(
            '/lessons/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': 1, 'name': 'Test', 'description': 'test', 'preview': None, 'video_link': None, 'course': 1,
             'owner': 1}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """ Тестирование просмотра списка уроков """
        course = Course.objects.create(
            name="Test course list",
            description="Test course list",
            owner=self.user
        )

        Lesson.objects.create(
            name="Test list",
            description="test list",
            course=course,
            owner=self.user
        )

        response = self.client.get(
            '/lessons/',
        )

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': Lesson.objects.first().id,  # Используем первый созданный урок
                    'name': 'Test list',
                    'description': 'test list',
                    'preview': None,
                    'video_link': None,
                    'course': course.id,  # Используем первичный ключ курса
                    'owner': self.user.id  # Используем первичный ключ пользователя
                }
            ]
        }

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            expected_data
        )

    def test_detail_lesson(self):
        """ Тестирование просмотра деталей урока """
        course = Course.objects.create(
            name="Test course detail",
            description="Test course detail",
            owner=self.user
        )

        lesson = Lesson.objects.create(
            name="Test detail",
            description="test detail",
            course=course,
            owner=self.user
        )

        url = f'/lessons/detail/{lesson.pk}/'

        response = self.client.get(url)

        expected_data = {
            'id': lesson.id,  # Используем первичный ключ урока
            'name': 'Test detail',
            'description': 'test detail',
            'preview': None,
            'video_link': None,
            'course': course.id,  # Используем первичный ключ курса
            'owner': self.user.id  # Используем первичный ключ пользователя
        }

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            expected_data
        )

    def test_delete_lesson(self):
        """ Тестирование удаления урока """
        # Создаем тестовый курс и урок
        course = Course.objects.create(
            name="Test delete",
            description="Test delete",
            owner=self.user
        )

        lesson = Lesson.objects.create(
            name="Test delete",
            description="test delete",
            course=course,
            owner=self.user
        )

        url = f'/lessons/delete/{lesson.pk}/'


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что урок был удален из базы данных
        self.assertFalse(Lesson.objects.filter(pk=lesson.pk).exists())

class SubscriptionViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        """ Тестирование подписки """
        course = Course.objects.create(
            name="Test subscription",
            description="Test subscription",
            owner=self.user
        )

        data = {
            "course": course.pk
        }

        response = self.client.post('/subscription/', data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Subscription.objects.filter(user=self.user, course=course).exists())

    def test_delete_subscription(self):
        """ Тестирование удаления подписки """
        course = Course.objects.create(
            name="Test subscription",
            description="Test subscription",
            owner=self.user
        )

        subscription = Subscription.objects.create(user=self.user, course=course)

        url = f'/unsubscribe/{course.pk}/'

        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Subscription.objects.filter(pk=subscription.pk).exists())
