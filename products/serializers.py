from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.pagination import PageNumberPagination
from .models import Category, Product, ProductImages
from django.core.files.storage import default_storage

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
      return default_storage.url(productImage.image_url.name)
    return None
  


class ProductSerializer(ModelSerializer):
  productImage = SerializerMethodField()
  class Meta:
    model = Product
    fields = ['product_id', 'name', 'price', 'discount_price', 'description', 'sku', 'productImage']
  
  def get_productImage(self, obj):
    images_qs = getattr(obj, 'products_productimages_product_id', obj.products_productimages_product_id).order_by('-is_primary')
    return ProductImagesSerializer(images_qs, many=True).data


# class SubCategorySerializer(ModelSerializer):
#   # products = ProductsSerializer(source='products_product_category_id',many=True, read_only=True)
#   subcategories = SerializerMethodField()

#   class Meta:
#     model = Category
#     fields = ['category_id', 'name', 'Icon', 'slug', 'subcategories']

#   def get_subcategories(self, obj):
#     qs = obj.products_category_parent_category_id.all()
#     return CategorySerializer(qs, many=True).data


# class CategorySerializer(ModelSerializer):
#   products = ProductsSerializer(source='products_product_category_id',many=True, read_only=True)
#   # sub_categories = SubCategorySerializer(many=True, read_only=True)
#   class Meta:
#     model = Category
#     fields = ['name', 'Icon', 'category_id', 'slug', 'products',]

class CategorySerializer(ModelSerializer):
  subcategories = SerializerMethodField()
  # products = ProductsSerializer(source='leaf_products', many=True, read_only=True)
  products = SerializerMethodField()



  class Meta:
    model = Category
    fields = ['name', 'Icon', 'parent_category_id', 'category_id', 'slug', 'subcategories', 'products', 'level']
    read_only_fields = ['category_id', 'level']
  

  def get_subcategories(self, obj):
    include_children = self.context.get('include_children', False)
    if not include_children:
        return None
    return CategorySerializer(
        obj.products_category_parent_category_id.all(),  # Eager-load products for children
        many=True,
        context=self.context,
        read_only=True
    ).data
  
  def get_products(self, obj):
    include_products = self.context.get('include_products', False)
    has_children = obj.products_category_parent_category_id.exists()
    if has_children or not include_products:
        return []

    # Paginate here: Mimic DRF pagination for nested
    products_qs = obj.products_product_category_id.all()
    paginator = PageNumberPagination()
    paginator.page_size = 20  # Or from context/request
    page = self.context.get('page', 1)  # Default first page; pass from view if needed
    try:
        paginated_products = paginator.paginate_queryset(products_qs, self.context['request'], view=None)
    except Exception:
        paginated_products = products_qs[:20]  # Fallback slice

    serializer = ProductsSerializer(paginated_products, many=True, context=self.context)
    data = serializer.data

    # Add pagination metadata for "load more"
    return {
        'results': data,
        'count': products_qs.count(),  # Total for progress bar
        'next': page + 1 if len(data) == 20 else None,  # Simple next page flag
        'has_more': len(data) == 20
    }
  
