import coreapi
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from order.models import Order, OrderStatus
from order.serializers import OrderSerializer


class OrderList(ListAPIView):

    queryset = Order.objects.select_related('status', 'restaurant')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    @swagger_auto_schema(responses={200: {}, 400: {}})
    def list(self, request):
        queryset = self.get_queryset()
        order_status = self.request.GET.get('status', None)
        if order_status:
            try:
                status_id = OrderStatus.objects.get(status=order_status)
                queryset = queryset.filter(status=status_id)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
