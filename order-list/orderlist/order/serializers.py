from rest_framework import serializers
from order.models import Order
from food.serializers import FoodSerializer


class OrderSerializer(serializers.ModelSerializer):

    user = serializers.CharField()
    status = serializers.CharField()
    restaurant = serializers.CharField()
    food_items = FoodSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'restaurant', 'status', 'food_items']
