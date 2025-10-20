from django.contrib import admin
from .models import Orders, OrderItems, OrderTaxes, OrderShipping, Returns, ReturnItems

admin.site.register([Orders, OrderItems, OrderTaxes, OrderShipping, Returns, ReturnItems])