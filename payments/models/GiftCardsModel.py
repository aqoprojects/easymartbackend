from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class GiftCards(models.Model, DateModel):
  gift_card_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

  code = models.UUIDField(default=uuid.uuid4, unique=True)
  balance = models.DecimalField(max_digits=10, decimal_places=2)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")

  issue_date = models.DateTimeField()
  expiry_date = models.DateTimeField()
  is_active = models.BooleanField()
  

  def str(self):
    return "This is GiftCards data"
