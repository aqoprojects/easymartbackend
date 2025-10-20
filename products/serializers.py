from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Product

class CategorySerializer(ModelSerializer):
  class Meta:
    model = Category
    fields = ['name', 'Icon']

class ProductsSerializer(ModelSerializer):
  productImage = SerializerMethodField()
  class Meta:
    model = Product
    fields = ['product_id', 'name', 'price', 'discount_price', 'product_slug', 'productImage']
  
  def get_productImage(self, obj):
    productImage = obj.products_productimages_product_id.get(is_primary=True)
    if productImage:
      request = self.context.get('request')
      return request.build_absolute_uri(productImage.image_url.url) if request else productImage.image_url.url
    return None


class ProductSerializer(ModelSerializer):
  class Meta:
    model = Product
    fields = ['product_id', 'name', 'price', 'discount_price', 'description', 'sku']