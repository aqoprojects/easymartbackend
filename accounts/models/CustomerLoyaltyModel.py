from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.LoyaltyProgramsModel import LoyaltyPrograms


class CustomerLoyalty(models.Model, DateModel):
  customer_loyalty_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  loyal_program_id = models.ForeignKey(LoyaltyPrograms, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_loyal_program_id")
  points_balance = models.IntegerField()
  tier = models.CharField(max_length=20, choices=[("tier", "Gold Silver Bronze")])

  def str(self):
    return "This is CustomerLoyalty data"

