from django.db import models
from restaurant.models import Restaurant

class FoodCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(FoodCategory, on_delete=models.PROTECT, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)    

    def __str__(self):
        return self.name