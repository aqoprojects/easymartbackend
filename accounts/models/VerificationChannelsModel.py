from django.db import models
import uuid
from django.conf import settings
from accounts.models.DateModel import DateModel
from accounts.models.VerificationTokenModel import VerificationToken


class VerificationChannel(DateModel):
  channel_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  names = models.CharField(max_length=30)
  method = models.CharField(max_length=10, choices=[('sms', 'Sms'), ('email', 'Email'), ('push', 'Push')])
  api_key = models.CharField(max_length=50)
  is_active = models.BooleanField()
  priority = models.IntegerField()

  def str(self):
    return "This is verification channel data"

