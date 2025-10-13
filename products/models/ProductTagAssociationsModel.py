from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from products.models.ProductModel import Product
from products.models.ProductTagsModel import ProductTags

class ProductTagAssociations(DateModel):
  product_tag_association_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  tag_id = models.ForeignKey(ProductTags, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_tag_id")
  


  def str(self):
    return "This is ProductTagAssociations data"
