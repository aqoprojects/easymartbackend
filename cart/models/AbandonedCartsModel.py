from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from cart.models.CartModel import Cart


class AbandonedCarts(DateModel):
  abandoned_carts_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_cart_id")
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  last_activity_at = models.DateTimeField()
  status = models.CharField(max_length=20, choices=[("status", "abandoned recovered converted")])
  notification_sent = models.BooleanField()
  

  def str(self):
    return "This is AbandonedCarts data"
