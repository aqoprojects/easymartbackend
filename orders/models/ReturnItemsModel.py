from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.ReturnsModel import Returns
from customer.models.OrderItemsModel import OrderItems                    
class ReturnItems(models.Model, DateModel):
  return_item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  return_id = models.ForeignKey(Returns, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_return_id")
  order_item_id = models.ForeignKey(OrderItems, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_item_id")
  quantity = models.IntegerField()
  condition = models.CharField(max_length=20, choices=[("condition", "new used damaged notworking malfunctioning")])

  def str(self):
    return "This is ReturnItems data"
