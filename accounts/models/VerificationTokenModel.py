from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel



class VerificationToken(DateModel):
  token_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  token = models.CharField(max_length=4, unique=True)
  type = models.CharField(max_length=20, choices=[('email verification', 'Email verification'), ('password reset', 'Password reset'), ('phone verification', 'Phone verification'), ('2fa', '2FA')])
  channel = models.CharField(max_length=10, choices=[('email', 'Email'), ('sms', 'Sms'), ('app', 'App')])
  expires_at = models.DateTimeField()
  is_used = models.BooleanField(default=False)  
  metadata = models.JSONField(null=True, blank=True)

  def str(self):
    return "This is verification token data"

