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
            "other_titles": "new_other_title",
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
        }

        response = self.client.patch(update_url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pereval1.refresh_from_db()
        self.assertEqual(self.pereval1.title, 'test1title')

    def test_get_list_pereval(self):
        url = reverse("pereval-list")
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval1, ], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_single_pereval(self):
        url = reverse("pereval-detail", args=(self.pereval1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_pereval(self):
        delete_url = reverse('pereval-detail', args=[self.pereval1.id])

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pereval.objects.filter(id=self.pereval1.id).exists())

    def test_pereval_update(self):
        url = reverse("pereval-detail", args=(self.pereval1.id,))
        data = {
            "id": 1,
            "beauty_title": "new_pereval",
            "title": "new_title",
            "other_titles": "new_other_title",
            "connect": "new_connect",
            "user": {
                "email": "test@mail.ru",
                "fam": "Петров",
                "name": "Петр",
                "otc": "Петрович",
                "phone": "89997777777"
            },
            "coords": {
                "latitude": "33.33",
                "longitude": "33.33",
                "hight": "3333.33"
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
        }
        json_data = json.dumps(data)
        response = self.client.patch(path=url, content_type='application/json', data=json_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.pereval1.refresh_from_db()
        self.assertEqual("test1pereval", self.pereval1.beauty_title)


class PerevalSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email="test1@mail.ru",
            fam="test1fam",
            name="test1name",
            otc="test1otc",
            phone="test1phone"
        )
        self.coords1 = Coordinates.objects.create(
            latitude=11.11,
            longitude=11.11,
            height=1111.00
        )
        self.level1 = Level.objects.create(
            winter="1А",
            summer="1А",
            autumn="1А",
            spring="1А",
        )
        self.pereval1 = Pereval.objects.create(
            beauty_title="test1pereval",
            title="test1title",
            other_titles="test1other",
            connect="test1connect",
            user=self.user1,
            coords=self.coords1,
            level=self.level1
        )
        self.images1 = Images.objects.create(
            pereval=self.pereval1,
            data="http://127.0.0.1:8000//media/photos/название-pereval_id4.jpeg",
            title="название"
        )
        self.images2 = Images.objects.create(
            pereval=self.pereval1,
            data="http://127.0.0.1:8000//media/photos/название-pereval_id4.jpeg",
            title="название"
        )

    def test_check(self):
        serializer_data = PerevalSerializer(self.pereval1).data
        expected_data = {
            "id": 1,
            "beauty_title": "test1pereval",
            "title": "test1title",
            "other_titles": "test1other",
            "connect": "test1connect",
            "user": {
                "email": "test1@mail.ru",
                "fam": "test1fam",
                "name": "test1name",
                "otc": "test1otc",
                "phone": "test1phone"
            },
            "coords": {
                "latitude": "11.11",
                "longitude": "11.11",
                "height": "1111.00"
            },
            "level": {
                "winter": "1А",
                "summer": "1А",
                "autumn": "1А",
                "spring": "1А"
            },
            "images": [
                {
                    "data": "http://127.0.0.1:8000//media/photos/название-pereval_id4.jpeg",
                    "title": "название"
                },
                {
                    "data": "http://127.0.0.1:8000//media/photos/название-pereval_id4.jpeg",
                    "title": "название"
                }
            ],
            "status": "new"
        }

        print("Сериализованные данные:", serializer_data)
        print("Ожидаемые данные:", expected_data)
        self.assertEqual(serializer_data, expected_data)
