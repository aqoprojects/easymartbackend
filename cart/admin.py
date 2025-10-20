from django.contrib import admin
from .models import Cart,CartItems,AbandonedCarts

admin.site.register([Cart, CartItems, AbandonedCarts])
