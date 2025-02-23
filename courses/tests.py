from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Course, Lesson
from users.models import User


class CoursesTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email="user@test.com", password=123)
        self.client.force_authenticate(user=self.user)


    def test_create_lesson(self):
        """ Тестирование создания уроков """
        url = reverse('courses:lesson-create')
        data = {
            "title":"test lesson",
            "description":"test description",
            "url":"http://youtube.com"
        }

        response =self.client.post(
            url,
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

        self.assertEqual(
            Lesson.objects.count(),
            1
        )

    def test_update_lesson(self):
        """Тестирование обновления уроков"""
        self.lesson = Lesson.objects.create(
            title="nontest",
            description="nontest",
            url="http://youtube.com"
        )


        urlpath = reverse('courses:lesson-update', kwargs={"pk": self.lesson.pk})
        data = {
            "title": "test lesson",
            "description": "test description",
            "url": "http://youtube.com"
        }

        response = self.client.patch(
            urlpath,
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_lesson(self):
        """Тестирование получения одного урока"""
        self.lesson = Lesson.objects.create(
            title="nontest",
            description="nontest",
            url="http://youtube.com"
        )
        urlpath = reverse('courses:lesson-get', kwargs={"pk": self.lesson.pk})

        response = self.client.get(
            urlpath
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_lesson_list(self):
        """Тестирование получения всех уроков"""
        Lesson.objects.create(
            title="nontest",
            description="nontest",
            url="http://youtube.com"
        )
        urlpath = reverse('courses:lesson-list')
        response = self.client.get(
            urlpath
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_destroy_lesson(self):
        """Тестирование удаления урока"""
        self.lesson = Lesson.objects.create(
            title="nontest",
            description="nontest",
            url="http://youtube.com"
        )

        urlpath = reverse('courses:lesson-delete', kwargs={"pk": self.lesson.pk})
        response = self.client.delete(
            urlpath
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )