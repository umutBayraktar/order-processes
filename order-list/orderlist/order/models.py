from django.db import models
from django.conf import settings
from food.models import Food
from restaurant.models import Restaurant


class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    food_items = models.ManyToManyField(Food)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.username
