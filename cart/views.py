from django.shortcuts import render
from rest_framework import generics, status, serializers
from .models import Cart, CartItems
from .serializers import CartSerializer, CartItemsSerializer
from rest_framework.response import Response
from django.db.models import Sum
import stripe 
from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from orders.models import Orders, OrderItems 
from utils.cart import guest_perform_add_to_cart, guest_create_add_to_cart, get_guest_carts, guest_perform_cart_update, get_guest_cartitems_data_through_cart, get_guest_cartitems_data, guest_perform_cart_delete, guest_destroy_cart_delete, get_customer_cartitems_data, get_customer_carts, customer_perform_add_to_cart, customer_create_add_to_cart, customer_perform_cart_update, get_customer_cartitems_data_through_cart, customer_perform_cart_delete, customer_destroy_cart_delete




stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secrets = settings.WEBHOOK_SECRET

class CartApi(generics.ListCreateAPIView):
  queryset = Cart.objects.prefetch_related('cart_cartitems_cart_id').all()
  serializer_class  = CartSerializer

  def list(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      guest_id = self.request.COOKIES.get('guest_id')
      if not guest_id:
        return Response({'cart_cartitems_cart_id': [], "order_items":[], 'total_items': 0}, status=200)  
         
      cart = Cart.objects.get(guest_id=guest_id) 
      response = get_guest_cartitems_data(cart.cart_id)
      print(response)
      return Response(response)
    else:
      response = get_customer_cartitems_data(self)
      return Response(response)



class CartItemsApi(generics.ListCreateAPIView):
  serializer_class  = CartItemsSerializer

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      queryset = get_guest_carts(self)
    else:
      queryset = get_customer_carts(self)
    return queryset



class CartCreateApi(generics.CreateAPIView):
  serializer_class = CartItemsSerializer

  def perform_create(self, serializer):
    if not self.request.user.is_authenticated:
      print("WWE@@")
      guest_perform_add_to_cart(self, serializer)
    else:
      customer_perform_add_to_cart(self, serializer)


  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    if not request.user.is_authenticated:
      print("WWE")
      response = guest_create_add_to_cart(self, request, response)
    else:
      response = customer_create_add_to_cart(self, response)
    return response 


class CartUpdateApi(generics.UpdateAPIView):
  serializer_class = CartItemsSerializer
  lookup_url_kwarg = 'cart_item_id'

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      queryset = get_guest_carts(self)
    else:
      queryset = get_customer_carts(self)
    return queryset
 

  def perform_update(self, serializer):
    if not self.request.user.is_authenticated:
      guest_perform_cart_update(serializer)
    else:
      customer_perform_cart_update(serializer)



  def update(self, request, *args, **kwargs):
    response = super().update(request, *args, **kwargs)
    if not request.user.is_authenticated:
      response = get_guest_cartitems_data_through_cart(request, response)
    else:
      response = get_customer_cartitems_data_through_cart(request, response)
    return response

class CartDeleteApi(generics.DestroyAPIView):
  serializer_class = CartItemsSerializer
  lookup_url_kwarg = 'cart_item_id'

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      queryset = get_guest_carts(self)
    else:
      queryset = get_customer_carts(self)
      
    return queryset
  
  def perform_destroy(self, instance):
    if not self.request.user.is_authenticated:
      guest_perform_cart_delete(instance)
    else:
      customer_perform_cart_delete(instance)
      

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)

    if not self.request.user.is_authenticated:
      response = guest_destroy_cart_delete(instance)
    else:
      response = customer_destroy_cart_delete(self, instance)
    return response


class create_checkout_session(generics.GenericAPIView):

  def post(self, request):
    print("HEERE")
    customer = request.user
    try:
      cart = Cart.objects.get(customer_id=customer)
    except Cart.DoesNotExist:
      return Response({"error": "No active cart found"}, status=404)

    try:
      checkout_session = stripe.checkout.Session.create(
        customer_email=customer.email,
        payment_method_types=['card'],
          line_items=[
              {
                  'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.product_id.name},
                    'unit_amount': int(item.product_id.price) * 100,
                  },
                  'quantity': item.quantity,
              }

              for item in cart.cart_cartitems_cart_id.all()
          ],
          mode='payment',
          success_url='https://sport-news-r9zz.onrender.com/',
          cancel_url='https://sport-news-r9zz.onrender.com/news/oba-femi-makes-tony-dangelo-watch-his-family-suffe/',
          metadata = {'cart_id': str(cart.cart_id)}
      )
      # print("HERE2")
      return Response({"url": checkout_session.url})
    except Exception as e:
      return Response({"error": str(e)}, status=400)


class StripeWebhookView(APIView):
  """
  Handle Stripe webhooks (checkout.session.completed, etc.).
  No authentication required - secured by signature verification.
  """
  permission_classes = [AllowAny]  # Stripe calls this publicly

  def post(self, request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = endpoint_secrets  

    if not sig_header:
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print("Stripe webhook error - invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print("Stripe webhook error - invalid signature:", e)
        return HttpResponse(status=400)

    # Handle specific events
    if event['type'] in ['checkout.session.completed', 'checkout.session.async_payment_succeeded']:
        session = event['data']['object']
        cart_id = session.get('metadata', {}).get('cart_id')  # Use cart_id (string)

        if cart_id:
            fulfill_checkout(session)
        else:
            print("Webhook received but no cart_id in metadata")

    # Add more events as needed (e.g., payment failed, subscription events)
    # elif event['type'] == 'invoice.payment_failed':
    #     ...

    return HttpResponse(status=200)


# def fulfill_checkout(session, cart_code):

#   order = Orders.objects.get(
#     # stripe_checkout_id=session["id"],
#     # amount = session['amount_total'],
#     customer_id__email=session['customer_email'],
#     # status="Processing",
#   )
#   order.status = "Processing"


#   # cart =Cart.objects.get(cart_code=cart_code)
#   # cartitems = cart.cartitems.all()

#   # for item in cartitems:
#   #   orderitem = OderItem.objects.create(
#   #     order=order, product=item.product, quantity=item.quantity
#   #   )

#   order.save()
#   # cart.delete()

def fulfill_checkout(session):
  """
  Fulfill the order after successful payment.
  Run this in a Celery task in production for reliability.
  """
  try:
      # Better: Retrieve session with expand to get line items if needed
      # session = stripe.checkout.Session.retrieve(session['id'], expand=['line_items'])

      # Find or create order - use session.id (unique) to avoid duplicates
      order = Orders.objects.get(
          # stripe_checkout_id=session['id'],
          customer_id = get_user_model().objects.get(email=session['customer_email']),
              # 'amount': session['amount_total'] / 100,  # Convert cents
              # 'currency': session['currency'],
              # 'status': 'Paid',  # Or 'Processing'
          
      )
      # order.status = 'Processing'
      # order.save()

      # if not created:
      #     # Already processed (idempotent - safe for retries)
      #     print(f"Order {order.id} already fulfilled for session {session['id']}")
      #     return

      # # Optional: Transfer cart items to order items
      # cart_id = session.get('metadata', {}).get('cart_id')
      # if cart_id:
      #     try:
      #         cart = Cart.objects.get(cart_id=cart_id, customer_id__email=session['customer_email'])
      #         for item in cart.cart_cartitems_cart_id.all():
      #             OrderItem.objects.create(
      #                 order=order,
      #                 product=item.product_id,
      #                 quantity=item.quantity,
      #                 price=item.product_id.price  # Snapshot price
      #             )
      #         cart.delete()  # Clear cart after success
      #     except Cart.DoesNotExist:
      #         print("Cart not found for fulfillment")

      order.status = 'Processing'  # Or 'Paid'
      order.save()

      # print(f"Order {order.id} fulfilled successfully for session {session['id']}")

  except Exception as e:
      print("Error fulfilling checkout:", e)
      # In production: Log to Sentry/Rollbar, maybe retry with Celery