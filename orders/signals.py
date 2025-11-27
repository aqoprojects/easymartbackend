from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from cart.models import CartItems
from orders.models import Orders, OrderItems
from django.db.models import Sum


@receiver(post_save, sender=CartItems)
def create_or_update_order(sender, instance, created, **kwargs):
  cart_itmes = instance.cart_id.cart_cartitems_cart_id.all() 
  
  order, created = Orders.objects.get_or_create(cart_id=instance.cart_id)
  get_orderitem_subtotal = instance.quantity * instance.product_id.price

  orderItems, created = OrderItems.objects.get_or_create(order_id=order, product_id=instance.product_id)
  orderItems.quantity = instance.quantity
  orderItems.unit_price = instance.product_id.price
  orderItems.subtotal = round(get_orderitem_subtotal, 2)
  orderItems.save()

  get_order_total = order.orders_orderitems_order_id.aggregate(total_quantity=Sum('subtotal'))
  order.total_amount = round(get_order_total['total_quantity'],2)
  order.save()

@receiver(post_delete, sender=CartItems)
def delete_order(sender, instance, **kwargs):
  # cart_itmes = instance.cart_id.cart_cartitems_cart_id.all() 
  
  order = Orders.objects.get(cart_id=instance.cart_id)
  # get_orderitem_subtotal = instance.quantity * instance.product_id.price

  orderItems = OrderItems.objects.get(order_id=order, product_id=instance.product_id)
  orderItems.delete()

  if order.orders_orderitems_order_id.count() <=0:
    order.delete()
    return
  get_order_total = order.orders_orderitems_order_id.aggregate(total_quantity=Sum('subtotal'))
  order.total_amount = round(get_order_total['total_quantity'],2)
  order.save()