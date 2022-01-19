from restaurant.models import Restaurant
from food.models import Food
from django.db import models
from manage import init_django
from django.contrib.auth.models import User

init_django()


class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    food_items = models.ManyToManyField(Food)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.username
