from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product 
from customer.models.PromotionsModel import Promotions

class ProductPromotions(models.Model, DateModel):
  product_promotion_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  promotion_id = models.ForeignKey(Promotions, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_promotion_id")



  def str(self):
    return f"{self.product_promotion_id} for {self.product_id.name}"
