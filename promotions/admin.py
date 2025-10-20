from django.contrib import admin
from .models import Promotions, DynamicPricingRules, ProductPromotions

admin.site.register([Promotions, DynamicPricingRules, ProductPromotions])