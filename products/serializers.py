from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Category, Product, ProductImages

class CategorySerializer(ModelSerializer):
  class Meta:
    model = Category
    fields = ['name', 'Icon', 'category_id']


class ProductImagesSerializer(ModelSerializer):
  class Meta:
    model = ProductImages
    fields = ["image_id", "image_url", "is_primary", "alt_text"]
    # exclude = ["image_id"]



class ProductsSerializer(ModelSerializer):
  productImage = SerializerMethodField()
  class Meta:
    model = Product
    fields = ['product_id', 'name', 'price', 'discount_price', 'product_slug', 'productImage']
  
  def get_productImage(self, obj):
    productImage = obj.products_productimages_product_id.get(is_primary=True)
    if productImage:
      request = self.context.get('request')
      return request.build_absolute_uri(productImage.image_url.url) if request else 'http://localhost:8000'+productImage.image_url.url
    return None


class ProductSerializer(ModelSerializer):
  productImage = SerializerMethodField()
  class Meta:
    model = Product
    fields = ['product_id', 'name', 'price', 'discount_price', 'description', 'sku', 'productImage']
  
  def get_productImage(self, obj):
    images_qs = getattr(obj, 'products_productimages_product_id', obj.products_productimages_product_id).order_by('-is_primary')
    return ProductImagesSerializer(images_qs, many=True).data