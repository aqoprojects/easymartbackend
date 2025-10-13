from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.OrdersModel import Orders

class Payments(models.Model, DateModel):
  payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id")
  payment_method = models.CharField(max_length=50)
  amount  = models.DecimalField(max_digits=10, decimal_places=2)
  payment_status = models.CharField(max_length=20, choices=[("payment_status", "pending completed failed refunded processing")])
  transaction_id = models.CharField(max_length=200)
  payment_date = models.DateTimeField()

  def str(self):
    return f"order {self.order_id} payment is {self.payment_status}"
