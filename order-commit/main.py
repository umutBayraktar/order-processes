import ast
import json
from rabbitmq.connector import RabbitMQConnector
from django.contrib.auth.models import User
from order.models import Order, OrderStatus
from food.models import Food
from restaurant.models import Restaurant
from manage import init_django

init_django()


def check_message_values(message_dict):

    user_value = message_dict.get('user', None)
    restaurant_value = message_dict.get('restaurant', None)
    items_value = message_dict.get('items', None)
    status_value = message_dict.get('status', None)

    if user_value and restaurant_value and items_value and status_value:
        if type(user_value) != int or type(restaurant_value) != int or type(status_value) != int:
            return False
        if type(items_value) != type([]):
            return False
        else:
            int_check = all(isinstance(n, int) for n in items_value)
            return int_check
    else:
        return False


def write_database(ch, method, properties, body):
    body = ast.literal_eval(body.decode("utf-8"))
    if check_message_values(body):
        user = body.get("user", None)
        restaurant = body.get("restaurant", None)
        food_items = tuple(body.get("items"))
        status = body.get("status", None)
        try:
            user = User.objects.get(pk=user)
            restaurant = Restaurant.objects.get(pk=restaurant)
            foods = Food.objects.filter(id__in=food_items)
            status = OrderStatus.objects.get(pk=status)
            order = Order.objects.create(
                user=user, restaurant=restaurant, status=status)
            order.save()
            for food in foods:
                order.food_items.add(food)
        except Exception:
            print("An exception occurred while the order creation process")
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connector = RabbitMQConnector(host='localhost')
    connector.set_consumer('orders', write_database)
    connector.start_consume()
