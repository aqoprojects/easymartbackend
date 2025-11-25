from cart.models import Cart, CartItems
from .cartitems_data import get_cartitems_data
from rest_framework.exceptions import ValidationError
import uuid 

def guest_perform_add_to_cart(self, serializer):
  guest_id = self.request.COOKIES.get('guest_id')
  try:
    cart_id = Cart.objects.get(guest_id=guest_id)
  except:
    cart_id = Cart.objects.create(guest_id=uuid.uuid4())
    
  validated_data = serializer.validated_data
  product_id = validated_data['product_id']
  add_quantity = validated_data.get('quantity', 1)
  
  cart_item, created = CartItems.objects.get_or_create(cart_id=cart_id, product_id=product_id)
  cart_item.quantity += add_quantity
  cart_item.save()
  serializer.instance = cart_item


def guest_create_add_to_cart(self, request, response):
  cart_id = Cart.objects.get(cart_id=response.data.get('cart_id'))
  response.data = get_cartitems_data(cart_id)
  guest_id = self.request.COOKIES.get('guest_id')
  try:
    validate_guest_id = Cart.objects.get(guest_id=guest_id)
  except:
    validate_guest_id = None
  print(validate_guest_id)
  if 'guest_id' not in request.COOKIES or validate_guest_id is None:
    response.set_cookie('guest_id', cart_id.guest_id, httponly=True, samesite='Lax')
    print("wwe")
  return response

def get_guest_carts(self):
  guest_id = self.request.COOKIES.get('guest_id')
  queryset = CartItems.objects.filter(cart_id__guest_id=guest_id)
  return queryset


def guest_perform_cart_update(serializer):
  if 'quantity' not in serializer.validated_data:
    raise ValidationError("Quantity is required for update.")

  quantity = serializer.validated_data['quantity']
  if quantity <= 0:
    raise ValidationError("Quantity cannot be lesser than one.")

  serializer.save()