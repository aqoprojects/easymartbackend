from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class Promotions(models.Model, DateModel):
  promotion_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=200)
  description = models.TextField(max_length=500)
  discount_type = models.CharField(max_length=20, choices=[("discount_type", "percentage fixed")])
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  is_active = models.BooleanField()

  def str(self):
    return f"{self.name} is {f"active and ends on {self.end_date}" if self.is_active else "not active"}"
  
