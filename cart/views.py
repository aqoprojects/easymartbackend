from django.shortcuts import render
from rest_framework import generics, status, serializers
from .models import Cart, CartItems
from .serializers import CartSerializer, CartItemsSerializer
from rest_framework.response import Response
from django.db.models import Sum
from utils.cart import guest_perform_add_to_cart, guest_create_add_to_cart, get_guest_carts, guest_perform_cart_update, get_cartitems_data_through_cart, get_cartitems_data, guest_perform_cart_delete, guest_destroy_cart_delete


class CartApi(generics.ListCreateAPIView):
  queryset = Cart.objects.prefetch_related('cart_cartitems_cart_id').all()
  serializer_class  = CartSerializer

  def list(self, request, *args, **kwargs):
    guest_id = self.request.COOKIES.get('guest_id')
    if not guest_id:
      return Response({'items': [], 'total': 0}, status=200)  
        
    try:
      cart = Cart.objects.get(guest_id=guest_id) 
      response = get_cartitems_data(cart.cart_id)
      print("wwe")
      return Response(response)
    except Cart.DoesNotExist:
      return Response({'items': [], 'total': 0}, status=404)  
    
    except Cart.MultipleObjectsReturned:
      cart = Cart.objects.filter(guest_id=guest_id).first()
      serializer = self.get_serializer(cart)
      return Response(serializer.data)



class CartItemsApi(generics.ListCreateAPIView):
  serializer_class  = CartItemsSerializer

  def get_queryset(self):
    guest_id = self.request.COOKIES.get('guest_id')
    queryset = CartItems.objects.filter(cart_id__guest_id=self.request.COOKIES.get('guest_id'))
    return queryset



class CartCreateApi(generics.CreateAPIView):
  serializer_class = CartItemsSerializer

  def perform_create(self, serializer):
    if not self.request.user.is_authenticated:
      guest_perform_add_to_cart(self, serializer)

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    if not request.user.is_authenticated:
      response = guest_create_add_to_cart(self, request, response)
    return response 


class CartUpdateApi(generics.UpdateAPIView):
  serializer_class = CartItemsSerializer
  lookup_url_kwarg = 'cart_item_id'

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      queryset = get_guest_carts(self)
    return queryset
 

  def perform_update(self, serializer):
    if not self.request.user.is_authenticated:
      guest_perform_cart_update(serializer)


  def update(self, request, *args, **kwargs):
    response = super().update(request, *args, **kwargs)
    if not request.user.is_authenticated:
      response = get_cartitems_data_through_cart(request, response)
    return response

class CartDeleteApi(generics.DestroyAPIView):
  serializer_class = CartItemsSerializer
  lookup_url_kwarg = 'cart_item_id'

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      queryset = get_guest_carts(self)
    return queryset
  
  def perform_destroy(self, instance):
    if not self.request.user.is_authenticated:
      guest_perform_cart_delete(instance)
      print("Yoo1")

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()  # gets the CartItem
    self.perform_destroy(instance)
    print("YOO2")
    response = guest_destroy_cart_delete(instance)
    print("YOO5")
    return response