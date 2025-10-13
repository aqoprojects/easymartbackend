from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from customer.models.DateModel import DateModel
from customer.models.CustomerSupportTicketsModel import CustomerSupportTickets                    

class CustomerSupportResponses(models.Model, DateModel):
  customer_support_response_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  ticket_id = models.ForeignKey(CustomerSupportTickets, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_ticket_id")
  # responder_id = models.ForeignKey(null=True, blank=True)
  message = models.TextField()

  def str(self):
    return f"responded to {self.ticket_id.customer_support_ticket_id}"
  
