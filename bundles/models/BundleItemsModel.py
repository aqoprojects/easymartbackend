from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductBundlesModel import ProductBundles
from customer.models.ProductModel import Product 

class BundleItems(models.Model, DateModel):
  bundle_item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

  bundle_id = models.ForeignKey(ProductBundles, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_bundle_id")
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  quantity = models.IntegerField()

  def str(self):
    return "This is BundleItems data"
