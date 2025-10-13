from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product


class ProductRankings(models.Model, DateModel):
  product_rankings_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  ranking_type = models.CharField(max_length=20 , choices=[("ranking_type", "best_selling trending top_selling")])
  score = models.DecimalField(max_digits=10, decimal_places=2)
  time_period = models.CharField(max_length=20, choices=[("time_period", "daily weekly monthly all_time")])
  rank = models.IntegerField()

  def str(self):
    return "This is ProductRankings data"
