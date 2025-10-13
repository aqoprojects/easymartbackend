from django.db import models
import uuid
from django.conf import settings
from accounts.models.DateModel import DateModel
from accounts.models.VerificationTokenModel import VerificationToken


class TwoFactorAuth(DateModel):
  tfa_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  method = models.CharField(max_length=10, choices=[('totp', 'Totp'), ('sms', 'Sms'), ('email', 'Email'), ('hardware token', 'Hardware token')])
  secret = models.CharField(max_length=30, null=True, blank=True)
  is_enabled = models.BooleanField()
  last_verified_at = models.DateTimeField(auto_now=True)
  backup_codes = models.JSONField(null=True, blank=True)

  def str(self):
    return "This is 2fa data"

