from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from orders.models.OrdersModel import Orders
# from shipping.models.ShippingMethodsModel import ShippingMethods

class OrderShipping(DateModel):
  order_shipping_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id")
  # shipping_method_id = models.ForeignKey(ShippingMethods, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_shipping_method_id", null=True, blank=True)

  tracking_number = models.IntegerField(null=True, blank=True)
  shipped_date = models.DateTimeField(null=True, blank=True)
  delivered_date = models.DateTimeField(null=True, blank=True)

  def str(self):
    return "This is OrderShipping data"
