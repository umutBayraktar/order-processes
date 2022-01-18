from django.contrib import admin
from order.models import Order, OrderStatus

admin.site.register(Order)
admin.site.register(OrderStatus)