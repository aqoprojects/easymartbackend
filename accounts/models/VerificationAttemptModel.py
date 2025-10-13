from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models.DateModel import DateModel
from accounts.models.VerificationTokenModel import VerificationToken


class VerificationAttempt(DateModel):
  attempt_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  token_id = models.ForeignKey(VerificationToken, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_token_id")
  customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_customer_id")
  token = models.CharField(max_length=4)
  attempt_status = models.CharField(max_length=10, choices=[('success', 'Success'), ('failure', 'Failure'), ('expired', 'Expired'), ('rate limited', 'Rate limited')])
  ip_address = models.CharField(max_length=60)
  user_agent = models.TextField(null=True, blank=True)

  def str(self):
    return "This is verification attempt data"

