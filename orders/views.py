from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Orders,OrderItems
from .serializers import OrderSerializer, OrderItemSerializer

class OrdersApi(generics.ListAPIView):
  serializer_class = OrderSerializer
  
  def list(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      guest_id = request.COOKIES.get('guest_id')
      if guest_id is None:
        return Response({"order_id": "629cdc8d-f552-4371-9214-3e3b53372d86",
    "total_amount": "0.00"})
      guest_order = Orders.objects.get(cart_id__guest_id=guest_id)
      serializer = self.get_serializer(guest_order)
      return Response(serializer.data)
    else:
      customer_order = Orders.objects.get(customer_id=request.user)
      serializer = self.get_serializer(customer_order)
      return Response(serializer.data)
