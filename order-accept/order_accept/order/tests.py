from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from pika import BlockingConnection, ConnectionParameters
from order.rabbitmq_connector import RabbitMQConnector


class OrderAcceptAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.api_url = '/api/v1/order/add/'
        self.correct_data = {'user': 1,
                             'restaurant': 1, 'status': 1, 'items': [1]}

    def test_get_request(self):
        response = self.client.get(self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_put_request(self):
        response = self.client.put(
            self.api_url, self.correct_data, format='json')
        self.assertEqual(response.status_code, 405)

    def test_patch_request(self):
        response = self.client.patch(
            self.api_url, self.correct_data, format='json')
        self.assertEqual(response.status_code, 405)

    def test_delete_request(self):
        response = self.client.delete(self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_post_request_missing_user_key(self):
        missing_user = {'restaurant': 1, 'status': 1, 'items': [1]}
        response = self.client.post(self.api_url, missing_user, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_missing_restaurant_key(self):
        missing_restautant = {'user': 1, 'status': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, missing_restautant, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_missing_status_key(self):
        missing_status = {'user': 1, 'restaurant': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, missing_status, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_missing_items_key(self):
        missing_items = {'user': 1, 'restaurant': 1, 'status': 1}
        response = self.client.post(self.api_url, missing_items, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_user_wrong_value_type(self):
        user_wrong_value = {'user': "s",
                            'restaurant': 1, 'status': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, user_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_restaurant_wrong_value_type(self):
        restaurant_wrong_value = {'user': 1,
                                  'restaurant': "s", 'status': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, restaurant_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_status_wrong_value_type(self):
        status_wrong_value = {'user': 1,
                              'restaurant': 1, 'status': "s", 'items': [1]}
        response = self.client.post(
            self.api_url, status_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_items_wrong_value_type_int(self):
        items_wrong_value = {'user': 1,
                             'restaurant': 1, 'status': 1, 'items': 1}
        response = self.client.post(
            self.api_url, items_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_items_wrong_value_type_str_list(self):
        items_wrong_value = {'user': 1, 'restaurant': 1,
                             'status': 1, 'items': ["s"]}
        response = self.client.post(
            self.api_url, items_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_items_wrong_value_type_str(self):
        items_wrong_value = {'user': 1,
                             'restaurant': 1, 'status': 1, 'items': "1"}
        response = self.client.post(
            self.api_url, items_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_items_wrong_value_empty_list(self):
        items_wrong_value = {'user': 1,
                             'restaurant': 1, 'status': 1, 'items': []}
        response = self.client.post(
            self.api_url, items_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_user_wrong_value_0(self):
        user_wrong_value = {'user': 0,
                            'restaurant': 1, 'status': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, user_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_restaurant_wrong_value_0(self):
        restaurant_wrong_value = {'user': 1,
                                  'restaurant': 0, 'status': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, restaurant_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_status_wrong_value_0(self):
        status_wrong_value = {'user': 1,
                              'restaurant': 1, 'status': 0, 'items': [1]}
        response = self.client.post(
            self.api_url, status_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_item_wrong_value_listitem_0(self):
        listitem_wrong_value = {'user': 1,
                                'restaurant': 1, 'status': 1, 'items': [0]}
        response = self.client.post(
            self.api_url, listitem_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_user_wrong_value_negative_int(self):
        user_wrong_value = {'user': -1,
                            'restaurant': 1, 'status': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, user_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_restaurant_wrong_value_negative_int(self):
        restaurant_wrong_value = {'user': 1,
                                  'restaurant': -1, 'status': 1, 'items': [1]}
        response = self.client.post(
            self.api_url, restaurant_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_status_wrong_value_negative_int(self):
        status_wrong_value = {'user': 1,
                              'restaurant': 1, 'status': -1, 'items': [1]}
        response = self.client.post(
            self.api_url, status_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_items_wrong_value_listitem_negative_int(self):
        listitem_wrong_value = {'user': 1,
                                'restaurant': 1, 'status': 1, 'items': [-1]}
        response = self.client.post(
            self.api_url, listitem_wrong_value, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_correct_values(self):
        conn = BlockingConnection(
            ConnectionParameters(host=settings.RABBITMQ_HOST))
        channel = conn.channel()

        response = self.client.post(
            self.api_url, self.correct_data, format='json')
        self.assertEqual(response.status_code, 201)

        def consume(ch, method, properties, body):
            import ast

            body = ast.literal_eval(body.decode("utf-8"))
            self.assertDictEqual(body, self.correct_data)
            channel.basic_cancel('test-consumer')

        channel.basic_consume(queue=settings.QUEUE_NAME,
                              on_message_callback=consume, consumer_tag='test-consumer')
        channel.start_consuming()


class RabbitMQConnectorTests(TestCase):

    def setUp(self):
        self.connector = RabbitMQConnector(host=settings.RABBITMQ_HOST)

    def test_send_message(self):
        test_message = "test"
        conn = BlockingConnection(
            ConnectionParameters(host=settings.RABBITMQ_HOST))
        channel = conn.channel()
        self.connector.send_message("test", test_message)

        def consume(ch, method, properties, body):
            body = body.decode("utf-8")
            self.assertEqual(body, test_message)
            channel.basic_cancel('test-consumer')
        channel.basic_consume(queue="test",
                              on_message_callback=consume, consumer_tag='test-consumer')
        channel.start_consuming()

    def test_set_consumer(self):
        test_message = "test"
        conn = BlockingConnection(
            ConnectionParameters(host=settings.RABBITMQ_HOST))
        channel = conn.channel()
        channel.basic_publish(
            exchange='', routing_key='test', body=test_message)

        def consume(ch, method, properties, body):
            body = body.decode("utf-8")
            self.assertEqual(body, test_message)
            self.connector.close()
        self.connector.set_consumer("test", consume)
        self.connector.start_consume()
