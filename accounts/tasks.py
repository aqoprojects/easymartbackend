from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import VerificationToken
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

@shared_task
def sendVerificationMail(customer_email, cutomer_id):
  customer = get_user_model().objects.get(email=customer_email)
  token = get_random_string(length=4, allowed_chars='0123456789')
  expires_at =timezone.now() + timedelta(minutes=5)
  VerificationToken.objects.create(customer_id=customer, token=token, expires_at=expires_at, type='email verification', channel='email')
  subject = "Verify account"
  body = f"this is your verification code: {token}"
  mail = EmailMultiAlternatives(
    subject=subject,
    body=body,
    from_email=settings.EMAIL_HOST_USER,
    to=[customer_email],
  )
  mail.send()
  return f"Mail sent to {customer}"