from orders.models import Orders, OrderItems
from rest_framework import serializers 

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Orders
    fields = ['order_id', 'total_aount']
    

class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItems
    fields = ['order_item_id', 'product_id', 'subtotal']
