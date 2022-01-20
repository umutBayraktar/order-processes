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

    connector = RabbitMQConnector(host=settings.RABBITMQ_HOST)

    @swagger_auto_schema(request_body=OrderSerializer, responses={200: {}, 400: {}})
    def post(self, request):

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            message = json.dumps(data)
            self.connector.send_message(settings.QUEUE_NAME, message)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
