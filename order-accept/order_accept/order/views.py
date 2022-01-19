from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from order.serializers import OrderSerializer
from order.rabbitmq_connector import RabbitMQConnector
import json


class AddOrder(APIView):

    connector = RabbitMQConnector(host="localhost")

    def post(self, request):

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            message = json.dumps(data)
            self.connector.send_message(settings.QUEUE_NAME, message)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
