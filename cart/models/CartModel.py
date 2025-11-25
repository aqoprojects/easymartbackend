from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from django.conf import settings


class Cart(DateModel):
  cart_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  guest_id = models.CharField(max_length=100, null=True, blank=True)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id",null=True, blank=True)
  


  def str(self):
    return self.cart_id
