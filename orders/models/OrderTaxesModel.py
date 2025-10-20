from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from orders.models.OrdersModel import Orders
# from taxes.models.TaxesModel import Taxes

class OrderTaxes(DateModel):
  order_tax_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id")
  # tax_id = models.ForeignKey(Taxes, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_tax_id")
  tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
  

  def str(self):
    return "This is OrderTaxes data"
