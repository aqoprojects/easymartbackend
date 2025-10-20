from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from accounts.models.AddressesModel import Addresses          


class Orders(DateModel):
  order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  order_date = models.DateTimeField(null=True, blank=True)
  status = models.CharField(max_length=20, choices=[("Status", "Pending Processing Shipped Delivered Cancelled")], help_text="should have a default of pending for order that has been created but not paid for, about to pe paid for, about to be palced . when placed proceed to processing")

  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
  # shipping_address_id = models.ForeignKey(Addresses, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s__shipping_address_id")
  # billing_address_id = models.ForeignKey(Addresses, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_billing_address_id")
  
  

  def str(self):
    return "This is Orders data"
