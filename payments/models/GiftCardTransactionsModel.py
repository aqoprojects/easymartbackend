from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.GiftCardsModel import GiftCards
from customer.models.OrdersModel import Orders


class GiftCardTransactions(models.Model, DateModel):
  gift_card_transaction_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  gift_card_id = models.ForeignKey(GiftCards, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_gift_card_id")
  order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_order_id")
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  transaction_type = models.CharField(max_length=20, choices=[("transaction_type", "issue refund redeem")])

  def str(self):
    return "This is GiftCardTransactions data"
