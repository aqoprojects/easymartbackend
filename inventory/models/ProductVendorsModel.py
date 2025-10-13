from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ProductModel import Product    
from customer.models.VendorsModel import Vendors


class ProductVendors(models.Model, DateModel):
  product_vendor_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")
  vendor_id = models.ForeignKey(Vendors, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_vendor_id")
  vendor_sku = models.CharField(max_length=20)
  cost_price = models.DecimalField(max_digits=10, decimal_places=2)
  lead_time_days = models.CharField(max_length=10, help_text="estimated lead time for restocking")

  def str(self):
    return f"{self.product_id.name} from {self.vendor_id.name}. skU: {self.vendor_sku}"
