from django.contrib import admin
from django.urls import path, include

from order.views import AddOrder

urlpatterns = [
    path('add/', AddOrder.as_view())
]
