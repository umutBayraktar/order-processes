from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

class OrderList(ListAPIView):

    def get(self, request):
        return Response({})
