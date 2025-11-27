from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Orders,OrderItems
from .serializers import OrderSerializer, OrderItemSerializer

class OrdersApi(generics.ListAPIView):
  serializer_class = OrderSerializer
  
  def list(self, request, *args, **kwargs):
    guest_id = request.COOKIES.get('guest_id')
    guest_order = Orders.objects.get(cart_id__guest_id=guest_id)
    serializer = self.get_serializer(guest_order)
    return Response(serializer.data)