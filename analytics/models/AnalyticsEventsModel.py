from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
                    
class AnalyticsEvents(DateModel):
  analytics_event_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id", null=True, blank=True)
  event_type_options = models.TextChoices("event_type", "page_view product_view add_to_cart search")
  event_type = models.CharField(max_length=20, choices=event_type_options)
  event_data = models.JSONField(null=True, blank=True)

  def str(self):
    return "This is AnalyticsEvents data"
