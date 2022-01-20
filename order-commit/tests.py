import json
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from pika import BlockingConnection, ConnectionParameters
from main import check_message_values, write_database
from order.models import Order
from order.models import OrderStatus
from food.models import Food
from restaurant.models import Restaurant
from rabbitmq.connector import RabbitMQConnector


class CommitMessageTest(TestCase):

    def test_check_empty_message(self):
        ret_value = check_message_values({})
        self.assertEqual(ret_value, False)

    def test_check_missing_user_key_in_message(self):
        wrong_data = {'restaurant': 1, 'status': 1, 'items': [1]}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_check_user_wrong_type(self):
        wrong_data = {'user': "1", 'restaurant': 1, 'status': 1, 'items': [1]}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_check_missing_restaurant_key_in_message(self):
        wrong_data = {'user': 1, 'status': 1, 'items': [1]}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_check_restaurant_wrong_type(self):
        wrong_data = {'user': 1, 'restaurant': "1", 'status': 1, 'items': [1]}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_missing_status_key_in_message(self):
        wrong_data = {'user': 1, 'restaurant': 1, 'items': [1]}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_check_status_wrong_type(self):
        wrong_data = {'user': 1, 'restaurant': 1, 'status': "1", 'items': [1]}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_missing_items_key_in_message(self):
        wrong_data = {'user': 1, 'restaurant': 1, 'status': 1}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_check_items_wrong_type(self):
        wrong_data = {'user': 1, 'restaurant': 1, 'status': 1, 'items': 1}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_check_items_key_wrong_element_type(self):
        wrong_data = {'user': 1, 'status': 1, 'items': ["1"]}
        ret_value = check_message_values(wrong_data)
        self.assertEqual(ret_value, False)

    def test_check_correct_message(self):
        correct_data = {'user': 1, 'restaurant': 1, 'status': 1, 'items': [1]}
        ret_value = check_message_values(correct_data)
        self.assertEqual(ret_value, True)

    def test_correct_message(self):

        user = User.objects.create(username='testuser', password='TEST.1234')
        restaurant = Restaurant.objects.create(name='testrestaurant')
        status = OrderStatus.objects.create(status='teststatus')
        food = Food.objects.create(
            name='testfood', description='testfood', price=25.00, restaurant=restaurant)
        correct_data = {'user': user.id, 'restaurant': restaurant.id,
                        'status': status.id, 'items': [food.id]}
        message = json.dumps(correct_data)

        conn = BlockingConnection(
            ConnectionParameters(host=settings.RABBITMQ_HOST))
        self.channel = conn.channel()

        def write_database_wrapper(ch, method, properties, body):
            write_database(ch, method, properties, body)
            self.channel.basic_cancel('test-consumer')
        orders = Order.objects.all()
        orders_length = len(orders)
        self.channel.basic_publish(
            exchange='', routing_key='test_correct', body=message)
        self.channel.basic_consume(queue="test_correct",
                                   on_message_callback=write_database_wrapper, consumer_tag='test-consumer')
        self.channel.start_consuming()
        orders_after = Order.objects.all()
        orders_after_length = len(orders_after)
        self.assertNotEqual(orders_length, orders_after_length)
