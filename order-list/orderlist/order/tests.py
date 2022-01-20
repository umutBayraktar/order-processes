from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from food.models import Food
from food.models import FoodCategory
from restaurant.models import Restaurant
from order.models import Order
from order.models import OrderStatus


class OrderListAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.api_url = '/api/v1/order/order-list/'
        self.status_api_url_wrong = '/api/v1/order/order-list/?status=abc'
        self.status_api_url_correct = '/api/v1/order/order-list/?status=teststatus2'

    def test_post_request(self):
        response = self.client.post(self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_put_request(self):
        response = self.client.put(
            self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_patch_request(self):
        response = self.client.patch(
            self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_delete_request(self):
        response = self.client.delete(self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_no_data_success(self):  # 200
        Order.objects.all().delete()
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)

    def test_has_data_success(self):  # 200
        user = User.objects.create(username='testuser', password='TEST.1234')
        restaurant = Restaurant.objects.create(name='testrestaurant')
        status = OrderStatus.objects.create(status='teststatus')
        category = FoodCategory.objects.create(name='testcategory')
        food = Food.objects.create(
            name='testfood', description='testfood', price=25.00, category=category, restaurant=restaurant)
        order = Order.objects.create(
            user=user, status=status, restaurant=restaurant)
        order.save()
        order.food_items.add(food)
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 200)
        expected_result = [{
            'user': 'testuser',
            'restaurant': 'testrestaurant',
            'status': 'teststatus',
            'food_items': [
                {
                    'name': 'testfood',
                    'category': 'testcategory'
                }
            ]
        }]
        self.assertListEqual(response.json(), expected_result)

    def test_has_data_filter_by_status_success(self):  # 200
        user = User.objects.create(username='testuser', password='TEST.1234')
        restaurant = Restaurant.objects.create(name='testrestaurant')
        status = OrderStatus.objects.create(status='teststatus')
        status_2 = OrderStatus.objects.create(status='teststatus2')
        category = FoodCategory.objects.create(name='testcategory')
        food = Food.objects.create(
            name='testfood', description='testfood', price=25.00, category=category, restaurant=restaurant)
        food_2 = Food.objects.create(
            name='testfood2', description='testfood2', price=30.00, category=category, restaurant=restaurant)
        order = Order.objects.create(
            user=user, status=status, restaurant=restaurant)
        order.save()
        order.food_items.add(food)
        order.food_items.add(food_2)
        order_2 = Order.objects.create(
            user=user, status=status_2, restaurant=restaurant)
        order_2.save()
        order_2.food_items.add(food)
        order_3 = Order.objects.create(
            user=user, status=status_2, restaurant=restaurant)
        order_3.save()
        order_3.food_items.add(food)
        order_3.food_items.add(food_2)
        response = self.client.get(self.status_api_url_correct)
        self.assertEqual(response.status_code, 200)
        expected_result = [{
            'user': 'testuser',
            'restaurant': 'testrestaurant',
            'status': 'teststatus2',
            'food_items': [
                {
                    'name': 'testfood',
                    'category': 'testcategory'
                }
            ]
        },
            {
            'user': 'testuser',
            'restaurant': 'testrestaurant',
            'status': 'teststatus2',
            'food_items': [
                {
                    'name': 'testfood',
                    'category': 'testcategory'
                },
                {
                    'name': 'testfood2',
                    'category': 'testcategory'
                }
            ]
        }
        ]
        self.assertListEqual(response.json(), expected_result)

    def test_has_data_empty_status(self):  # 400
        response = self.client.get(self.status_api_url_wrong)
        self.assertEqual(response.status_code, 400)
