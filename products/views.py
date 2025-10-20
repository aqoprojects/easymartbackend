from rest_framework import generics
from .models import Category, Product
from analytics.models import AnalyticsEvents
from .serializers import CategorySerializer,ProductsSerializer, ProductSerializer
from rest_framework.response import Response

class ProductCategories(generics.ListAPIView):
  serializer_class = CategorySerializer
  queryset = Category.objects.filter(parent_category_id=None)

class Products(generics.ListAPIView):
  serializer_class = ProductsSerializer
  queryset = Product.objects.filter(is_active=True, stock_quantity__gt=0).order_by('created_at')[:50]


class Product(generics.RetrieveUpdateAPIView):
  serializer_class = ProductSerializer
  queryset = Product.objects.all()
  lookup_field = 'product_slug'


  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    AnalyticsEvents.objects.create(
      event_type = "product_view",
      event_data = {"product_slug": instance.product_slug}
    )
    serializer = self.get_serializer(instance)
    return Response(serializer.data)
