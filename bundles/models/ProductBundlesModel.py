from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class ProductBundles(models.Model, DateModel):
  product_bundle_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

  name = models.CharField(max_length=200)
  description = models.TextField(max_length=500)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
  is_active = models.BooleanField()

  def str(self):
    return "This is ProductBundles data"
