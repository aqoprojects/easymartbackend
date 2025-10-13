from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from products.models.CategoryModel import Category
from accounts.models.DateModel import DateModel
                    
class Product(DateModel):
  product_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=500)
  description = models.TextField(null=True, blank=True)
  sku = models.CharField(max_length=40, null=True, blank=True)
  category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_category_id", null=True, blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
  stock_quantity = models.IntegerField(null=True, blank=True)
  is_active = models.BooleanField(default=True)



  def __str__(self):
    return f"{self.name} is  {"very" if self.is_active else "not"} available "



