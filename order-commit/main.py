from manage import init_django

init_django()

from restaurant.models import Restaurant
from food.models import Food
from order.models import Order, OrderStatus
from django.contrib.auth.models import User
from rabbitmq.connector import RabbitMQConnector
import json
import ast

def write_database(ch, method, properties, body):
    print(" [x] %r" % body)
    
    body = json.loads(body)
    print(f"body: {body}")
    user = int(body["user"]) # TODO : use .get and add key not found check
    restaurant = int(body["restaurant"])
    food_items = tuple(ast.literal_eval(body["items"]))
    status = 1 # body["status"]
    #import pdb; pdb.set_trace()
    try:
        user = User.objects.get(pk=user)
        restaurant = Restaurant.objects.get(pk=restaurant)
        foods = Food.objects.filter(id__in=food_items)
        status = OrderStatus.objects.get(pk=status)
        order = Order.objects.create(user=user, restaurant=restaurant,status=status)
        order.save()
        for food in foods:
            order.food_items.add(food)
    except:
        print("Hata olustu")
        

    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    connector = RabbitMQConnector(host='localhost')
    connector.set_consumer('orders', write_database)
    connector.start_consume()
    #rest = Restaurant.objects.create(name="test-restaurant")