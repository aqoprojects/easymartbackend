from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class AnalyticsEvents(models.Model, DateModel):
  analytics_event_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id", null=True, blank=True, default="annonymous")
  event_type = models.CharField(max_length=10, choices=[("event_type", "page_view product_view add_to_cart search")])
  event_data = models.JSONField()

  def str(self):
    return "This is AnalyticsEvents data"
