from rest_framework import generics
from .models import Category, Product
from analytics.models import ProductRankings
from django.db.models import Count
from analytics.models import AnalyticsEvents
from promotions.models import Promotions
from .serializers import CategorySerializer,ProductsSerializer, ProductSerializer
from rest_framework.response import Response


class ProductCategories(generics.ListAPIView):
  serializer_class = CategorySerializer
  queryset = Category.objects.filter(parent_category_id=None)

class Products(generics.ListAPIView):
  serializer_class = ProductsSerializer
  
  def list(self, request, *args, **kwargs):
    bestSelling = Product.objects.filter(analytics_productrankings_product_id__ranking_type='best_selling', analytics_productrankings_product_id__time_period='daily').order_by('-analytics_productrankings_product_id__rank', '-analytics_productrankings_product_id__score', 'analytics_productrankings_product_id__created_at')
    trending = Product.objects.filter(analytics_productrankings_product_id__ranking_type='trending', analytics_productrankings_product_id__time_period='daily').order_by('-analytics_productrankings_product_id__rank', '-analytics_productrankings_product_id__score', 'analytics_productrankings_product_id__created_at')
    promotions = Product.objects.filter()


    best_selling_total = bestSelling.count()
    trending_total = trending.count()
    best_selling_products = self.serializer_class(bestSelling[:30], many=True).data
    trending_products = self.serializer_class(trending[:30], many=True).data
    return Response({
      'total_bsProducts': best_selling_total,
      'best_selling': best_selling_products,
      'total_tProducts': trending_total,
      'trending': trending_products
    })


class ProductAPI(generics.RetrieveUpdateAPIView):
  serializer_class = ProductSerializer
  queryset = Product.objects.all()
  lookup_field = 'product_slug'


  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    AnalyticsEvents.objects.create(
      product_id = instance,
      event_type = "product_view",
      event_data = {"product_slug": instance.product_slug}
    )
    serializer = self.get_serializer(instance)
    return Response(serializer.data)
