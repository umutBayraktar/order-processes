from rest_framework import serializers


class OrderSerializer(serializers.Serializer):

    user = serializers.IntegerField()
    restaurant = serializers.IntegerField()
    items = serializers.ListField(child=serializers.IntegerField())
