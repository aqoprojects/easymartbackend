from rest_framework import serializers
from .models import Promotions, ProductPromotions
from products.serializers import ProductsSerializer

class ProductPromotionSerializer(serializers.ModelSerializer):
  product_id=ProductsSerializer(read_only=True)
  class Meta:
    model = ProductPromotions
    fields = ["product_promotion_id","product_id"]

class PromotionSerializer(serializers.ModelSerializer):
  products = serializers.SerializerMethodField()
  total_products = serializers.SerializerMethodField()
  class Meta:
    model = Promotions
    fields = ['name', 'description', 'discount_type', 'discount_value', 'start_date', 'end_date', 'total_products', 'products',
    ]

  def get_products(self, obj):
    product_promotions = obj.promotions_productpromotions_promotion_id.all()
    size = int(self.context['request'].GET.get('size'))
    products = [pp.product_id for pp in product_promotions[:size]]
    return ProductsSerializer(products, many=True).data

  def get_total_products(self, obj):
    product_promotions_qs = getattr(obj, 'promotions_productpromotions_promotion_id', obj.promotions_productpromotions_promotion_id)
    return product_promotions_qs.count()
