from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from wishlist.models.WishlistsModel import Wishlists 
from products.models.ProductModel import Product     

class WishlistItems(DateModel):
  wishlist_item_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  wishlist_id = models.ForeignKey(Wishlists, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_wishlist_id")
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_product_id")


  def str(self):
    return "This is WishlistItems data"
