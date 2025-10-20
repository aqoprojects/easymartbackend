from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from products.models.ProductModel import Product


class ProductRankingMetrics(DateModel):
  product_ranking_metrics_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  metric_type = models.CharField(max_length=20, choices=[("metric_type", "sales views add_to_cart wishlist_adds search_click")])
  value = models.DecimalField(max_digits=10, decimal_places=2)
  time_period = models.CharField(max_length=20, choices=[("time_period", "daily weekly monthly all_time")])


  def str(self):
    return "This is ProductRankingMetrics data"
