from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class DynamicPricingRules(models.Model, DateModel):
  dynamic_pricing_rule_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=70)
  condition = models.CharField(max_length=100)
  adjustment_type = models.CharField(max_length=30, choices=[("adjustment_type", "percentage", "fixed")])
  adjustment_value = models.IntegerField()
  start_date = models.DateTimeField()
  end_date = models.DateTimeField(null=True, blank=True)
  is_active = models.BooleanField()




  def str(self):
    return "This is DynamicPricingRules data"
