from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from cart.models.CartModel import Cart
from products.models.ProductModel import Product 

class CartItems(DateModel):
  cart_item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name="%(app_label)s_%(class)s_cart_id")
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  quantity = models.IntegerField(default=0)


  class Meta:
    unique_together = [['cart_id', 'product_id']]



  def str(self):
    return f"{self.cart_item_id}"
