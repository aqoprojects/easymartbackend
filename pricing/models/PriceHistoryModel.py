from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product


class PriceHistory(models.Model, DateModel):
  price_history_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  price = models.DecimalField(max_digits=10, decimal_places=2)
  discount_price = models.DecimalField(max_digits=10, decimal_places=2)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()

  def str(self):
    return "This is PriceHistory data"
