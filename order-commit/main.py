import ast
import json
from rabbitmq.connector import RabbitMQConnector
from django.contrib.auth.models import User
from order.models import Order, OrderStatus
from food.models import Food
from restaurant.models import Restaurant
from manage import init_django

init_django()


def write_database(ch, method, properties, body):
    print(" [x] %r" % body)
    import pdb
    pdb.set_trace()
    body = ast.literal_eval(body.decode("utf-8"))
    user = body.get("user", None)  # TO DO :add key not found check
    # TO DO : add key not found check
    restaurant = body.get("restaurant", None)
    food_items = tuple(body.get("items"))  # TO DO:add key not found check
    status = body.get("status", None)  # TO DO : use .get and

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
    except:
        print("Hata olustu")

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connector = RabbitMQConnector(host='localhost')
    connector.set_consumer('orders', write_database)
    connector.start_consume()
