from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
                    
class ProductTags(DateModel):
  product_tag_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=50)
  description = models.TextField(max_length=400, null=True, blank=True)


  def str(self):
    return "This is ProductTags data"
