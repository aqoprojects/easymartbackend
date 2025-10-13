from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.OrdersModel import Orders


class CustomerSupportTickets(models.Model, DateModel):
  customer_support_ticket_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id")
  subject = models.CharField(max_length=300)
  description = models.TextField(max_length=800)
  status = models.CharField(max_length=20, choices=[("status", "pending open in_progress resolved closed")])

  def str(self):
    return f"Ticket from {self.customer_id.get_fullname} is {self.status}"
