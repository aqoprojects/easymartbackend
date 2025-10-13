from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomerManager(BaseUserManager):
  def create_user(self, email, first_name, last_name, password=None):

    if not email:
      raise ValueError("Please Provide an Email Address")
    
    user = self.model(
      email=self.normalize_email(email),
      first_name=first_name,
      last_name=last_name,
    )

    user.set_password(password)
    user.save(using=self._db)
    return user 
  
  def create_superuser(self, email, first_name, last_name, password=None):
    user = self.create_user(
      email,
      first_name=first_name,
      last_name=last_name,
      password=password
    )
    user.is_superuser=True 
    user.is_admin=True 
    user.is_active=True
    user.save(using=self._db)
    return user 
  

                    
class Customer(AbstractBaseUser):
  customer_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  first_name = models.CharField(max_length=40)
  last_name = models.CharField(max_length=40)
  email = models.EmailField(max_length=200, unique=True)
  phone_number = models.CharField(max_length=10)
  biography = models.TextField(max_length=600, null=True, blank=True)
  # gender = models.CharField(max_length=)
  # profile_picture = models.ImageField()
  is_active = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  is_superuser = models.BooleanField(db_default=False)
  objects = CustomerManager()


  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  def get_fullname(self):
    return f"{self.first_name} {self.last_name}"
  

  def str(self):
    return f"{self.get_fullname}"
  
  def has_perm(self, perm, obj=None):
    return True 

  def has_module_perms(self, app_label):
    return True 
  

  @property
  def is_staff(self):
    return self.is_admin

