from django.forms import ValidationError
from rest_framework import serializers


class OrderSerializer(serializers.Serializer):

    user = serializers.IntegerField(required=True)
    restaurant = serializers.IntegerField(required=True)
    status = serializers.IntegerField(required=True)
    items = serializers.ListField(
        child=serializers.IntegerField(required=True), required=True)

    def validate(self, data):
        user_value = data["user"]
        restaurant_value = data["restaurant"]
        status_value = data["status"]
        items_value = data["items"]

        if type(user_value) != int:
            raise ValidationError({"user": "User value should be an integer"})
        elif user_value <= 0:
            raise ValidationError(
                {"user": "User value should be upper than 0"})

        if type(restaurant_value) != type(1):
            raise ValidationError(
                {"restaurant": "Restaurant value should be an integer"})
        elif restaurant_value <= 0:
            raise ValidationError(
                {"restaurant": "Restaurant value should be upper than 0"})

        if type(status_value) != int:
            raise ValidationError(
                {"status": "Status value should be an integer"})
        elif status_value <= 0:
            raise ValidationError(
                {"status": "Status value should be upper than 0"})

        if type(items_value) != type([]):
            raise ValidationError({"items": "Items value should be a list"})
        elif len(items_value) == 0:
            raise ValidationError({"items": "Items values can not be empty"})
        else:
            for item in items_value:
                if type(item) != int:
                    raise ValidationError(
                        {"items": "Items element should be an integer"})
                elif item <= 0:
                    raise ValidationError(
                        {"items": "Items element should be upper than 0"})
        return data
