from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product 


class Subscriptions(models.Model, DateModel):
  subscription_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  status = models.CharField(max_length=20, choices=[("status", "active paused cancelled")])
  billing_frequency = models.CharField(max_length=20, choices=[("billing_frequency", "weekly monthly yearly")])
  start_date = models.DateField()
  end_date = models.DateField()
  last_billed_at = models.DateField()


  def str(self):
    return "This is Subscriptions data"
