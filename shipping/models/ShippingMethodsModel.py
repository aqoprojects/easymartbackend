from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class ShippingMethods(models.Model, DateModel):
  shipping_method_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=30)
  description = models.TextField(max_length=500)
  cost = models.DecimalField(max_digits=10, decimal_places=2)
  estimated_delivery_days = models.CharField(max_length=20, help_text="change it to time field.. thats it correct form form like correct column field")


  def str(self):
    return f"{self.name}"
