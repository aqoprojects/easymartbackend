from rest_framework import serializers
from .models import Cart, CartItems
from products.serializers import ProductsSerializer


class CartItemsSerializer(serializers.ModelSerializer):
  # product_id = ProductSerializer()
  product = ProductsSerializer(source='product_id', read_only=True)
  class Meta:
    model = CartItems
    fields = ['cart_item_id','cart_id', 'product', 'product_id', 'quantity']
  


class CartSerializer(serializers.ModelSerializer):
  cart_cartitems_cart_id = CartItemsSerializer(many=True, read_only=True)
  class Meta:
    model = Cart
    fields = ['cart_cartitems_cart_id']
