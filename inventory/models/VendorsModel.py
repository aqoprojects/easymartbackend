from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
                    
class Vendors(models.Model, DateModel):
  vendor_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  name = models.CharField(max_length=50)
  contact_email = models.EmailField(max_length=200)
  contact_phone_number = models.CharField(max_length=11)
  address = models.TextField(max_length=300)
  is_active = models.BooleanField()


  def str(self):
    return f"{self.name} is active: {self.is_active}"
  
