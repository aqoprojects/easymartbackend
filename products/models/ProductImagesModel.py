from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from products.models.ProductModel import Product    


class ProductImages(DateModel):
  image_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  image_url = models.ImageField(upload_to='products/', max_length=500)
  is_primary = models.BooleanField(default=False)
  alt_text = models.CharField(max_length=100, null=True, blank=True)


  def str(self):
    return "This is ProductImages data"
