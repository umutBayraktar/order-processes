import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from order.serializers import OrderSerializer
from order.rabbitmq_connector import RabbitMQConnector


class AddOrder(APIView):

    host = settings.RABBITMQ_HOST
    port = settings.RABBITMQ_PORT
    user = settings.RABBITMQ_USER
    password = settings.RABBITMQ_PASSWORD
    virtual_host = settings.RABBITMQ_VIRTUALHOST
    connector = RabbitMQConnector(
        host=host, port=port, virtual_host=virtual_host, user=user, password=password)

    @swagger_auto_schema(request_body=OrderSerializer, responses={201: {}, 400: {}})
    def post(self, request):

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            message = json.dumps(data)
            self.connector.send_message(settings.QUEUE_NAME, message)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
