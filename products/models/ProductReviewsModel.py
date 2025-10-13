from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product 
from django.conf import settings


class ProductReviews(models.Model, DateModel):
  review_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  rating = models.IntegerField(help_text="add a chpice option to this column with values 1 t05 no decimals..")
  comment = models.TextField(max_length=500)
  is_verified = models.BooleanField()


  def str(self):
    return "This is ProductReviews data"
