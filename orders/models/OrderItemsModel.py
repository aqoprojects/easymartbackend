from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.OrdersModel import Orders
from customer.models.ProductModel import Product     

class OrderItems(models.Model, DateModel):
  order_item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id")
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  quantity = models.IntegerField()
  unit_price = models.DecimalField(max_digits=10, decimal_places=2)
  subtotal = models.DecimalField(max_digits=10, decimal_places=2)


  def str(self):
    return "This is OrderItems data"
