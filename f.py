from accounts.models import Customer
from products.models import Product
from cart.models import Cart, CartItems
from orders.models import Orders, OrderItems
from analytics.models import AnalyticsEvents,ProductRankings,ProductRankingMetrics, SearchHistory
import random
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Count, Q, F, FloatField, DecimalField, ExpressionWrapper, Func
from analytics.models import ProductRankings

def RunWHole():
  customer = Customer.objects.first()
  cartId = ''
  products = [random.choice(Product.objects.filter(price__gt=0)[:120])  for i in range(30)]
  cart = Cart.objects.create(customer_id=customer)
  t = 1
  f = 1
  for product in products:
    cartitem, created = CartItems.objects.get_or_create(cart_id=cart, product_id=product )
    cartitem.quantity = cartitem.quantity + 1 if cartitem.quantity > 0 else random.randint(1,10)
    cartitem.save()
    AnalyticsEvents.objects.create(customer_id=customer,event_type="product_view", event_data={"product_id": str(product.product_id)})
    AnalyticsEvents.objects.create(customer_id=customer,event_type="add_to_cart",  event_data={"product_id": str(product.product_id)})
    ddd = random.choice([True, False])
    if ddd == True:
      AnalyticsEvents.objects.create(customer_id=customer,event_type="search",  event_data={"product_id": str(product.product_id)}) 
      t += 1
    else:
      f += 1
  print("True: ",t)
  print("False: ",f)

  getcartId=cart.cart_id
  
  cartId = Cart.objects.get(cart_id=getcartId)
  order = Orders.objects.create(customer_id=customer, cart_id=cartId, order_date=timezone.now(), status="pending")
  for cart in cartId.cart_cartitems_cart_id.all():
    orderitem = OrderItems.objects.create(order_id=order, product_id=cart.product_id)
    orderitem.quantity = cartitem.quantity
    orderitem.unit_price = cart.product_id.price 
    orderitem.subtotal = cartitem.quantity * cart.product_id.price 
    orderitem.save()
  ota =  order.orders_orderitems_order_id.all().aggregate(total_amount=Sum('subtotal'))
  order.total_amount =ota['total_amount']
  order.status = "Delivered"
  order.save()

# from django.db.models import Sum
def runit():
  for i in range(320):
    print(f"{i} of 320 Started\n------------------")
    RunWHole()
    print(f"{i} of 320 Ended\n------------------")


def BS():
  current_datetime = timezone.now()
  daily = current_datetime - timedelta(hours=24)
  weekly = current_datetime - timedelta(weeks=1)
  monthly = current_datetime - relativedelta(months=1)
  score = 1
  rank = 1
  bestSelling = Product.objects.annotate(best_selling=Count('orders_orderitems_product_id')).filter(orders_orderitems_product_id__created_at__gte=daily).order_by('-best_selling')
  for product in bestSelling:
    ProductRankings.objects.create(product_id=product, ranking_type='best_selling', score=score, rank=rank, time_period='daily')
    score+=1
    rank+=1

def TP():
  current_datetime = timezone.now()
  daily = current_datetime - timedelta(hours=24)
  weekly = current_datetime - timedelta(weeks=1)
  monthly = current_datetime - relativedelta(months=1)
  products_with_stats = Product.objects.annotate(
    total_product_view=Count(
        'analytics_analyticsevents_product_id',
        filter=Q(analytics_analyticsevents_product_id__event_type='product_view', analytics_analyticsevents_product_id__created_at__gte=daily)
    ),
    total_add_to_cart=Count(
        'analytics_analyticsevents_product_id',
        filter=Q(analytics_analyticsevents_product_id__event_type='add_to_cart', analytics_analyticsevents_product_id__created_at__gte=daily)
    ),  total_search=Count(
        'analytics_analyticsevents_product_id',
        filter=Q(analytics_analyticsevents_product_id__event_type='search', analytics_analyticsevents_product_id__created_at__gte=daily)
    ),
    ).order_by( '-total_product_view', '-total_search', '-total_add_to_cart')

  # return products_with_stats
  for product in products_with_stats:
    print("STRTED")
    print(product)
    ProductRankingMetrics.objects.create(
      product_id=product,
      metric_type="views",
      value = product.total_product_view,
      time_period = "daily"
    )
    ProductRankingMetrics.objects.create(
      product_id=product,
      metric_type="add_to_cart",
      value = product.total_add_to_cart,
      time_period = "daily"
    )
    ProductRankingMetrics.objects.create(
      product_id=product,
      metric_type="search_click",
      value = product.total_search,
      time_period = "daily"
    )
    
    print("done")
  print("OKAY")
  # analytics = AnalyticsEvents.objects.all()
  # for analytic in analytics:
  #   product = Product.objects.get(product_id=analytic.event_data['product_id']) 
  #   analytic.product_id = product
  #   analytic.save() 
  
#   current_datetime = timezone.now()
#   daily = current_datetime - timedelta(hours=24)
#   weekly = current_datetime - timedelta(weeks=1)
#   monthly = current_datetime - relativedelta(months=1) 
#   trending = Product.objects.annotate(total_view=Sum(analytics_analyticsevents_product_id_event_type='product_view'), total_cart=Sum(analytics_analyticsevents_product_id_event_type='add_to_cart'), total_search=Sum(analytics_analyticsevents_product_id_event_type='search'))

  

#  Product.objects.annotate(
#   total_views=Count('analytics__analyticsevents_product_id', filter=Q(analytics__analyticsevents_product_id__event_type="product_view")),
#   total_add_to_cart=Count('analytics__analyticsevents_product_id', filter=Q(analytics__analyticsevents_product_id__event_type="add_to_cart"))
# )

class Round2(Func):
  function = "ROUND"
  arity = 2


def TPR():
  PRODUCT_VIEW_WORTH = 0.1
  PRODUCT_SERCH_WORTH = 0.5
  PRODUCT_ADD_TO_CART = 0.3
  product_scores = Product.objects.annotate(
    views_score=Sum(
       ExpressionWrapper(
     PRODUCT_VIEW_WORTH * F('analytics_productrankingmetrics_product_id__value'),
     output_field=DecimalField(max_digits=10, decimal_places=2)
        ),
        filter=Q(analytics_productrankingmetrics_product_id__metric_type='views'),
    ),
    add_to_cart_score=Sum(
        ExpressionWrapper(
        PRODUCT_ADD_TO_CART * F('analytics_productrankingmetrics_product_id__value'),
        output_field=DecimalField(max_digits=10, decimal_places=2)
        ),
        filter=Q(analytics_productrankingmetrics_product_id__metric_type='add_to_cart'),
       
    ),
    search_click_score=Sum(
        ExpressionWrapper(
        PRODUCT_SERCH_WORTH * F('analytics_productrankingmetrics_product_id__value'),
        output_field=DecimalField(max_digits=10, decimal_places=2)
        ),
        filter=Q(analytics_productrankingmetrics_product_id__metric_type='search_click'),

    ),
  ).annotate(
      total_score=Round2(F('views_score') + F('add_to_cart_score') + F('search_click_score'), 2, output_field=DecimalField(max_digits=10, decimal_places=2))
  ).order_by('-total_score')
  rank = 1
  for product in product_scores.exclude(total_score=None):
    ProductRankings.objects.create(product_id=product, ranking_type='trending', score=product.total_score, rank=rank, time_period='daily')
    rank+=1
