from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class NotificationTemplates(models.Model, DateModel):
  notification_template_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=200)
  channel = models.CharField(max_length=50, choices=[("channel", "email sms push in_app")])
  type = models.CharField(max_length=50, choices=[("type", "order_update promotion restock abandoned_cart price_drop wishlist_item_available ")])
  status = models.CharField(max_length=50, choices=[("status", "pending sent failed read")])
  subject = models.CharField(max_length=200)
  content = models.TextField()
  is_active = models.BooleanField()




  def str(self):
    return "This is NotificationTemplates data"
