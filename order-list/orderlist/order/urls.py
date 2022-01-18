from django.urls import path, include
from order.views import OrderList

urlpatterns = [
    path('order-list/', OrderList.as_view())
]
