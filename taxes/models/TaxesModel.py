from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class Taxes(models.Model, DateModel):
  tax_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

  region = models.CharField(max_length=100)
  tax_rate = models.DecimalField(max_digits=10, decimal_places=2)
  is_active = models.BooleanField()

  def str(self):
    return f"The tax rate for {self.region} is {self.tax_rate}.. active status: {self.is_active}"
  
