from django.test import TestCase
from django.conf import settings
from pika import BlockingConnection, ConnectionParameters
from rabbitmq.connector import RabbitMQConnector

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
        channel.queue_declare(queue='test_cs', durable=True)
        channel.basic_publish(
            exchange='', routing_key='test_cs', body=test_message)

        def consume(ch, method, properties, body):
            body = body.decode("utf-8")
            self.assertEqual(body, test_message)
            self.connector.close()
        self.connector.set_consumer("test_cs", consume)
        self.connector.start_consume()
