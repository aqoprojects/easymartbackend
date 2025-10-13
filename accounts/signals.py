from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .tasks import sendVerificationMail

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def customerAccountVerification(sender, instance, **kwargs):
  sendVerificationMail.delay(instance.email, instance.customer_id)