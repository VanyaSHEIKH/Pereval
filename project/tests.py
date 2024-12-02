import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from project.models import Pereval, User, Coordinates, Level, Images
from project.serializers import PerevalSerializer


# Commands: python manage.py test  - запуск всех тестов
#           python manage.py test project.tests.PerevalApiTestCase.test_create_pereval - запускает конкретный тест


class PerevalApiTestCase(APITestCase):
    def setUp(self):
        # Создание перевала
        self.user1 = User.objects.create(
            email='test1@mail.ru',
            fam='test1fam',
            name='test1name',
            otc='test1otc',
            phone='test1phone'
        )
        self.coords1 = Coordinates.objects.create(
            latitude=11.11,
            longitude=11.11,
            height=1111.00
        )
        self.level1 = Level.objects.create(
            winter="1A",
            summer="1A",
            autumn="1A",
            spring="1A",
        )
        self.pereval1 = Pereval.objects.create(
            beauty_title="test1pereval",
            title="test1title",
            connect="test1connect",
            user=self.user1,
            coords=self.coords1,
            level=self.level1
        )
        self.images1 = Images.objects.create(
            pereval=self.pereval1,
        )

        self.url = reverse('pereval-list')

    def test_create_pereval(self):
        data = {
            "beauty_title": "new_pereval",
            "title": "new_title",
            "connect": "new_connect",
            "user": {
                "email": self.user1.email,
                "fam": "Иванов",
                "name": "Иван",
                "otc": "Иваныч",
                "phone": "1234567890"
            },
            "coords": {
                "latitude": 22.22,
                "longitude": 22.22,
                "height": 2222.00
            },
            "level": {
                "winter": "2А",
                "summer": "2А",
                "autumn": "2А",
                "spring": "2А"
            },
            "images": [
                {
                    "data": "binary_string",
                    "title": "название"
                },
                {
                    "data": "binary_string",
                    "title": "название"
                }
            ],
            "status": "new"
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(response.data)

        self.assertEqual(Pereval.objects.count(), 2)

    def test_partial_update_pereval(self):
        update_url = reverse('pereval-detail', args=[self.pereval1.id])
        update_data = {
            'title': 'test1title',
            'fam': 'test1fam',
        }

        response = self.client.patch(update_url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pereval1.refresh_from_db()
        self.assertEqual(self.pereval1.title, 'test1title')
        self.assertEqual(self.pereval1.user.fam, 'test1fam')

    def test_get_pereval_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_pereval(self):
        detail_url = reverse('pereval-detail', args=[self.pereval1.id])

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.pereval1.title)

    def test_delete_pereval(self):
        delete_url = reverse('pereval-detail', args=[self.pereval1.id])

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверьте, что перевал действительно удален
        self.assertFalse(Pereval.objects.filter(id=self.pereval1.id).exists())
