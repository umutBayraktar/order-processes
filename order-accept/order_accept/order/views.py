from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from order.serializers import OrderSerializer
from order.rabbitmq_connector import RabbitMQConnector

class AddOrder(APIView):

    connector = RabbitMQConnector(host="localhost")

    def post(self, request):
        
        serializer = OrderSerializer(data=request.data)
        #import pdb; pdb.set_trace()
        if serializer.is_valid():
            self.connector.send_message("orders", str(serializer.data))
            return Response(serializer.data)
            
        return Response({})
