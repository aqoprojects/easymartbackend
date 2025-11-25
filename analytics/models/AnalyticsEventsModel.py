from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from products.models import Product
                    
class AnalyticsEvents(DateModel):
  analytics_event_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id", null=True, blank=True)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id", null=True, blank=True)
  event_type_options = models.TextChoices("event_type", "page_view product_view add_to_cart search")
  event_type = models.CharField(max_length=20, choices=event_type_options)
  event_data = models.JSONField(null=True, blank=True)

  def str(self):
    return "This is AnalyticsEvents data"

# product_events = AnalyticsEvents.objects.filter(    event_type__in=['product_view', 'add_to_cart', 'search'],    event_data__has_key='product_id')
# >>> aggregated = product_events.values('event_data__product_id').annotate(    total_views=Count('analytics_event_id', filter=Q(event_type='product_view')),    total_add_to_cart=Count('analytics_event_id', filter=Q(event_type='add_to_cart')), total_search=Count('analytics_event_id', filter=Q(event_type='search'))).order_by('-total_search', '-total_views', '-total_add_to_cart')