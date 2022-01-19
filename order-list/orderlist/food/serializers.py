from rest_framework import serializers
from food.models import Food


class FoodSerializer(serializers.ModelSerializer):

    category = serializers.CharField()

    class Meta:
        model = Food
        fields = ['name', 'category']
