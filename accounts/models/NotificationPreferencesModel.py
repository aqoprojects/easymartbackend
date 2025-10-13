from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
                    
class NotificationPreferences(DateModel):
  notification_preference_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  channel = models.CharField(max_length=50, choices=[("channel", "email sms push in_app")])
  notification_type = models.CharField(max_length=50, choices=[("notification_type",  "order_update promotion restock abandoned_cart price_drop wishlist_item_available ")])
  is_enable = models.BooleanField()
  
  

  def str(self):
    return "This is NotificationPreferences data"
