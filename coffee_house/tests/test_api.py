from rest_framework.test import APITestCase
from django.urls import reverse
from coffee_house.models import coffee
from coffee_house.serializer import CoffeeSerializer
from rest_framework import status


class GetAllCoffeeTest(APITestCase):
    def setUp(self):
        coffee.objects.create(name='Эспрессо', volume=0.5, price=215.9)
        coffee.objects.create(name='Капучино', volume=0.33, price=314)
        coffee.objects.create(name='Американо', volume=0.52, price=447)
        coffee.objects.create(name='Латте', volume=0.45, price=150)

    def test_get_all_coffee(self):
        response = self.client.get(reverse('api_coffee_list'))

        coffee_list = coffee.objects.all()
        serializer = CoffeeSerializer(coffee_list, many=True)
        serializer = {'coffee': serializer.data}

        self.assertEqual(response.data, serializer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCoffeeTest(APITestCase):
    def setUp(self):
        self.espresso = coffee.objects.create(name='Эспрессо', volume=0.5, price=215.9)
        self.capuccino = coffee.objects.create(name='Капучино', volume=0.33, price=314)
        self.americano = coffee.objects.create(name='Американо', volume=0.52, price=447)
        self.latte = coffee.objects.create(name='Латте', volume=0.45, price=150)

    def test_get_valid_single_coffee(self):
        response = self.client.get(reverse('api_coffee_detail', kwargs={'pk': self.americano.pk}))

        single_coffee = coffee.objects.get(pk=self.americano.pk)
        serializer = CoffeeSerializer(single_coffee)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_coffee(self):
        response = self.client.get(reverse('api_coffee_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCoffeeTest(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'name': 'Capuccino',
            'volume': 0.5,
            'price': 250
        }
        self.invalid_payload = {
            'name': '',
            'volume': 4,
        }

    def test_create_valid_coffee(self):
        response = self.client.post(reverse('api_coffee_list'), data=self.valid_payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_invalid_coffee(self):
        response = self.client.post(reverse('api_coffee_list'), data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCoffeeTest(APITestCase):
    def setUp(self):
        self.espresso = coffee.objects.create(name='Эспрессо', volume=0.5, price=215.9)
        self.capuccino = coffee.objects.create(name='Капучино', volume=0.33, price=314)

        self.valid_payload = {
            'name': 'Американо',
            'volume': 0.75,
            'price': 500
        }
        self.invalid_payload = {
            'name': '',
            'volume': 4,
        }

    def test_valid_update_coffee(self):
        response = self.client.put(reverse('api_coffee_detail', kwargs={'pk': self.capuccino.pk}),
                                   data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_invalid_update_coffee(self):
        response = self.client.put(reverse('api_coffee_detail', kwargs={'pk': self.capuccino.pk}),
                                   data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCoffeeTest(APITestCase):
    def setUp(self):
        self.espresso = coffee.objects.create(name='Эспрессо', volume=0.5, price=215.9)
        self.capuccino = coffee.objects.create(name='Капучино', volume=0.33, price=314)
        self.americano = coffee.objects.create(name='Американо', volume=0.52, price=447)
        self.latte = coffee.objects.create(name='Латте', volume=0.45, price=150)

    def test_valid_delete_coffee(self):
        response = self.client.delete(reverse('api_coffee_detail', kwargs={'pk': self.capuccino.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_coffee(self):
        response = self.client.delete(reverse('api_coffee_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
