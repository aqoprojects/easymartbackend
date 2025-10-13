from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class Notifications(models.Model, DateModel):
  notification_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  type = models.CharField(max_length=50, choices=[("type", "order_update promotion restock abandoned_cart price_drop wishlist_item_available ")])

  title = models.CharField(max_length=200)
  message = models.TextField()
  channel = models.CharField(max_length=50, choices=[("channel", "email sms push in_app")])
  status = models.CharField(max_length=50, choices=[("status", "pending sent failed read")])
  priority = models.CharField(max_length=20, choices=[("priority", "low medium high")])
  scheduled_at = models.DateTimeField(null=True, blank=True)
  sent_at = models.DateTimeField(null=True, blank=True)
  metadata = models.JSONField(null=True, blank=True)


  def str(self):
    return "This is Notifications data"
