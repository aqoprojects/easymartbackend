from cart.models import CartItems, Cart
from cart.serializers import CartItemsSerializer
from django.db.models import Sum
from django.core.exceptions import ValidationError
from orders.models import Orders
from orders.serializers import OrderItemSerializer

def get_guest_cartitems_data(cart_id):
  try:
    cart_items = CartItems.objects.filter(cart_id=cart_id)
    cart_item_serializer = CartItemsSerializer(cart_items, many=True)
    cart_total_items = cart_items.aggregate(total_quantity=Sum('quantity'))
    order_items = Orders.objects.get(cart_id=cart_id).orders_orderitems_order_id.all()
    order_items_serializer = OrderItemSerializer(order_items, many=True)
    return {'cart_cartitems_cart_id': cart_item_serializer.data, "order_items":order_items_serializer.data, 'total_items': cart_total_items['total_quantity']}
  except CartItems.DoesNotExist:
    return {'cart_cartitems_cart_id': [], "order_items":[], 'total_items': 0}

def get_guest_cartitems_data_through_cart(request, response):
  try:
    guest_id = request.COOKIES.get('guest_id')
  except:
    raise ValidationError("Quantity is required for update.")
  
  cart_id = Cart.objects.get(guest_id=guest_id)
  cart_items = CartItems.objects.filter(cart_id=cart_id)
  cart_item_serializer = CartItemsSerializer(cart_items, many=True)
  cart_total_items = cart_items.aggregate(total_quantity=Sum('quantity'))
  order_items = Orders.objects.get(cart_id=cart_id).orders_orderitems_order_id.all()
  order_items_serializer = OrderItemSerializer(order_items, many=True)
  response.data =  {'cart_cartitems_cart_id': cart_item_serializer.data, "order_items":order_items_serializer.data, 'total_items': cart_total_items['total_quantity']}
  return response


def get_customer_cartitems_data(self):
  try:
    cart_id = Cart.objects.get(customer_id=self.request.user)
    cart_items = CartItems.objects.filter(cart_id=cart_id)
    cart_item_serializer = CartItemsSerializer(cart_items, many=True)
    cart_total_items = cart_items.aggregate(total_quantity=Sum('quantity'))
    order_items = Orders.objects.get(cart_id=cart_id).orders_orderitems_order_id.all()  
    order_items_serializer = OrderItemSerializer(order_items, many=True)
    print(cart_items)
    return {'cart_cartitems_cart_id': cart_item_serializer.data, "order_items":order_items_serializer.data, 'total_items': cart_total_items['total_quantity']}
  except (Cart.DoesNotExist, CartItems.DoesNotExist):
    return {'cart_cartitems_cart_id': [], "order_items":[], 'total_items': 0}