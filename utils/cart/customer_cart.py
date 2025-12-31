from cart.models import Cart, CartItems
import uuid 
from .cartitems_data import get_customer_cartitems_data
from rest_framework.exceptions import ValidationError
from cart.serializers import CartItemsSerializer
from orders.models import Orders
from orders.serializers import OrderItemSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

def get_customer_carts(self):
  queryset = CartItems.objects.filter(cart_id__customer_id=self.request.user) 
  return queryset


def customer_perform_add_to_cart(self, serializer):
  cart_id, created = Cart.objects.get_or_create(customer_id=self.request.user)
  validated_data = serializer.validated_data
  product_id = validated_data['product_id']
  add_quantity = validated_data.get('quantity', 1)
  
  cart_item, created = CartItems.objects.get_or_create(cart_id=cart_id, product_id=product_id)
  cart_item.quantity += add_quantity
  cart_item.save()
  serializer.instance = cart_item


def customer_create_add_to_cart(self, response):
  response.data = get_customer_cartitems_data(self)
  return response


def customer_perform_cart_update(serializer):
  if 'quantity' not in serializer.validated_data:
    raise ValidationError("Quantity is required for update.")

  quantity = serializer.validated_data['quantity']
  if quantity <= 0:
    raise ValidationError("Quantity cannot be lesser than one.")

  serializer.save()


def get_customer_cartitems_data_through_cart(request, response):
  cart_id = Cart.objects.get(customer_id=request.user)
  cart_items = CartItems.objects.filter(cart_id=cart_id)
  cart_item_serializer = CartItemsSerializer(cart_items, many=True)
  cart_total_items = cart_items.aggregate(total_quantity=Sum('quantity'))
  order_items = Orders.objects.get(cart_id=cart_id).orders_orderitems_order_id.all()
  order_items_serializer = OrderItemSerializer(order_items, many=True)
  response.data =  {'cart_cartitems_cart_id': cart_item_serializer.data, "order_items":order_items_serializer.data, 'total_items': cart_total_items['total_quantity']}
  print("WWE",order_items_serializer.data)
  return response


def customer_perform_cart_delete(instance):
  instance.delete()


def customer_destroy_cart_delete(self, instance):
  cart_id = instance.cart_id 
  is_last_cart_item = cart_id.cart_cartitems_cart_id.count()
  if is_last_cart_item <= 0:
    cart_id.delete()

    response = Response({
        "cart_cartitems_cart_id": [],   # or whatever you want
        "order_items": [],
        "total_items": 0
    })
    
    return response
  response = get_customer_cartitems_data(self)
  return Response(response)


def find_guest_cart(self, user):
  guest_id = self.request.COOKIES.get('guest_id')
  if guest_id is None:
    return 
  
  user_cart, created = Cart.objects.get_or_create(customer_id=user)
  guest_cart = Cart.objects.filter(guest_id=guest_id, customer_id=None).first()

  if guest_cart:
    for g_item in guest_cart.cart_cartitems_cart_id.all():
      try:
        user_item = user_cart.cart_cartitems_cart_id.get(product_id=g_item.product_id)
        user_item.quantity += g_item.quantity
        user_item.save()
      except CartItems.DoesNotExist:
        CartItems.objects.create(
          cart_id=user_cart,
          product_id=g_item.product_id,
          quantity=g_item.quantity
        )
    
    guest_cart.delete()


