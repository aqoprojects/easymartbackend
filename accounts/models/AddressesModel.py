from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
          
class Addresses(DateModel):
  address_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  address_title = models.CharField(max_length=100, null=True, blank=True)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  address_type = models.CharField(max_length=20, choices=[("AddressType", "Shipping Billing")])
  street_address = models.CharField(max_length=250)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  postal_code = models.CharField(max_length=20)
  country = models.CharField(max_length=50)
  is_default = models.BooleanField(default=False)




  def str(self):
    return f"{self.address_title} / {self.address_type} address of {self.customer_id.get_fullname}"
