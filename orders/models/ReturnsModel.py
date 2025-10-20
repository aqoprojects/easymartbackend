from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from orders.models.OrdersModel import Orders


class Returns(DateModel):
  return_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id")
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  status = models.CharField(max_length=20, choices=[("status", "requested approved rejected completed")])
  reason = models.TextField(max_length=500)

  def str(self):
    return "This is Returns data"
