from django.db import models
import uuid

from django.conf import settings
from accounts.models.DateModel import DateModel



class VerificationToken(DateModel):
  log_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  action = models.CharField(max_length=10, choices=[('token generated', 'Token generated'), ('token sent', 'Token sent'), ('attempt made', 'Attempt made'), ('verification success', 'Verification success'), ('verification failure', 'Verification failure')])
  detail = models.TextField(null=True, blank=True)

  def str(self):
    return "This is verification log data"

