from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from django.core.validators import FileExtensionValidator
from utils.products.validators import validate_Icon_size
class Category(DateModel):
  category_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  Icon = models.ImageField(upload_to='categoryIcon/', validators=[FileExtensionValidator(allowed_extensions=['svg']), validate_Icon_size], null=True, blank=True)
  parent_category_id = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name="%(app_label)s_%(class)s_parent_category_id")
  name = models.CharField(max_length=70)
  description = models.TextField(max_length=100, null=True, blank=True)


  def __str__(self):
    return f"{self.parent_category_id if self.parent_category_id is not None else ""}: {self.name}"
