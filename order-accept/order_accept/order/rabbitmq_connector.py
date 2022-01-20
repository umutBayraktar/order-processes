import pika


class RabbitMQConnector:

    def __init__(self, host='localhost', port=5672, virtual_host='/', user='guest', password='guest'):
        "Constructor"
        self.credentials = pika.PlainCredentials(user, password)
        if host == 'localhost':
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host))
        else:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host, port, virtual_host, self.credentials))

        self.channel = self.connection.channel()

    def send_message(self, queue_name, message):
        "Send message to queue"
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

    def set_consumer(self, queue_name, callback, auto_ack=False):
        "Consume messages from queue"
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=auto_ack)

    def start_consume(self):
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
