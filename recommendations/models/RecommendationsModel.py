from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product


class Recommendations(models.Model, DateModel):
  recommendation_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  recommendation_type = models.CharField(max_length=20, choices=[("recommendation_type", "frequently_bought_together", "similar_products", "based_on_history", "trending")])

  score = models.DecimalField(max_digits=10, decimal_places=2)
  expirs_at = models.DateTimeField(null=True, blank=True)



  def str(self):
    return "This is Recommendations data"
