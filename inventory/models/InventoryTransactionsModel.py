from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product  
from customer.models.OrdersModel import Orders

class InventoryTransactions(models.Model, DateModel):
  inventory_transaction_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  transaction_type = models.CharField(max_length=50)
  quantity = models.IntegerField()
  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id", null=True, blank=True)


  def str(self):
    return "This is InventoryTransactions data"
