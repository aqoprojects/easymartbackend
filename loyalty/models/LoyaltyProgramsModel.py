from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class LoyaltyPrograms(models.Model, DateModel):
  loyalty_programs_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=100)
  description = models.TextField()
  points_per_purchase = models.IntegerField()
  minimum_point_to_redeem = models.IntegerField()
  is_active = models.BooleanField()


  def str(self):
    return "This is LoyaltyPrograms data"
