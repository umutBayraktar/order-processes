from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from order.serializers import OrderSerializer
from order.rabbitmq_connector import RabbitMQConnector
import json

class AddOrder(APIView):

    connector = RabbitMQConnector(host="localhost")

    def post(self, request):
        
        serializer = OrderSerializer(data=request.data)
        #import pdb; pdb.set_trace()
        if serializer.is_valid():
            data = serializer.data
            for key in data.keys():
                data[key] = str(data[key])
            message = json.dumps(data)
            self.connector.send_message("orders", message)
            return Response(serializer.data)
            
        return Response({})
