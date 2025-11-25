from django.shortcuts import render
from rest_framework import generics
from .models import Promotions, ProductPromotions
from .serializers import PromotionSerializer, ProductPromotionSerializer
from django.db.models import Count
# Create your views here.


class Promotion(generics.ListAPIView):
  serializer_class = PromotionSerializer
  queryset = Promotions.objects.prefetch_related('promotions_productpromotions_promotion_id__product_id').filter(is_active=True)
  