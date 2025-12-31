from rest_framework import generics
from .models import Category, Product
from analytics.models import ProductRankings
from django.db.models import Count
from analytics.models import AnalyticsEvents
from django.db.models import Prefetch
from promotions.models import Promotions
from .serializers import ProductsSerializer, ProductSerializer, CategorySerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Case, When, Value, IntegerField
from django.db.models.functions import Concat, Substr

class StandardPagination(PageNumberPagination):
  page_size = 20
  page_size_query_param = 'page_size'
  max_page_size = 100

class ProductPagination(PageNumberPagination):
  page_size = 30  # Default; override with ?page_size=50
  page_size_query_param = 'page_size'
  max_page_size = 100

class SearchPagination(PageNumberPagination):
  page_size = 20
  page_size_query_param = 'page_size'
  max_page_size = 100

class TopLevelCategoryListView(generics.ListAPIView):
  queryset = Category.objects.filter(parent_category_id__isnull=True).prefetch_related(
      Prefetch('products_category_parent_category_id', queryset=Category.objects.prefetch_related('products_product_category_id'))
  )
  serializer_class = CategorySerializer
  pagination_class = StandardPagination
  # permission_classes = [IsAuthenticatedOrReadOnly]

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['request'] = self.request
    # Pass page for nested (default 1)
    context['page'] = int(self.request.query_params.get('page', 1))
    include_children_str = self.request.query_params.get('include_children', 'false')
    context['include_children'] = include_children_str.lower() == 'true'
    include_products_str = self.request.query_params.get('include_products', 'false')
    context['include_products'] = include_products_str.lower() == 'true'
    return context

  # @method_decorator(cache_page(60 * 15))  # Cache 15 min for static category tree
  def get(self, *args, **kwargs):
    response = super().get(*args, **kwargs)
    # Logs top-level fields
    
    return response 
  
class CategoryChildrenListView(generics.ListAPIView):
  serializer_class = CategorySerializer
  # permission_classes = [IsAuthenticatedOrReadOnly]
  pagination_class = StandardPagination

  def get_queryset(self):
    category_id = self.kwargs['pk']
    parent = Category.objects.get(category_id=category_id)
    include_products_str = self.request.query_params.get('include_products', 'false')  # String default here too
    include_products = include_products_str.lower() == 'true'
    prefetch = Prefetch('products_product_category_id') if include_products else None
    return parent.products_category_parent_category_id.prefetch_related(prefetch)

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['include_children'] = False  # No deeper nesting here
    # FIXED: String default
    include_products_str = self.request.query_params.get('include_products', 'false')
    context['include_products'] = include_products_str.lower() == 'true'
    return context

class CategoryProductsListView(generics.ListAPIView):
  serializer_class = ProductsSerializer
  pagination_class = StandardPagination
  # permission_classes = [IsAuthenticatedOrReadOnly]

  def get_queryset(self):
    category_id = self.kwargs['pk']
    queryset = Product.objects.filter(category_id=category_id)
    on_sale_str = self.request.query_params.get('on_sale', 'false')  # Consistent string handling
    if on_sale_str.lower() == 'true':
      queryset = queryset.filter(is_active=True)
    return queryset.select_related('category_id')  # Optimize FK access


  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['request'] = self.request  # For images
    return context

  # Optional: Add total count in response
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    response.data['total_count'] = self.get_queryset().count()  # For UI progress
    return response


# Optional: Single category detail (with optional nesting)
class CategoryDetailView(generics.RetrieveAPIView):
  queryset = Category.objects.prefetch_related(
      Prefetch('products_category_parent_category_id', queryset=Category.objects.prefetch_related('products_product_category_id'))
  )
  serializer_class = CategorySerializer
  # lookup_url_kwarg=
  # permission_classes = [IsAuthenticatedOrReadOnly]

  def get_serializer_context(self):
    context = super().get_serializer_context()
    include_children_str = self.request.query_params.get('include_children', 'false')
    context['include_children'] = include_children_str.lower() == 'true'
    include_products_str = self.request.query_params.get('include_products', 'false')
    context['include_products'] = include_products_str.lower() == 'true'
    return context
# class CategoriesApi(generics.ListAPIView):
#   serializer_class = CategorySerializer
#   queryset = Category.objects.filter(parent_category_id=None)

# class SubCategoryApi(generics.ListAPIView):
#   serializer_class = SubCategorySerializer
#   lookup_url_kwarg = "cat"

#   def get_queryset(self):
#     return Category.objects.filter(parent_category_id__slug=self.kwargs["cat"])
    

# class ProductSubCategories(generics.RetrieveAPIView):
#   # queryset = Category.objects.all()
#   serializer_class = SubCategorySerializer
  
#   def get(self, request, cat, sub_cat=None):
#     if sub_cat:
#         category = get_object_or_404(Category, parent_category_id__slug=cat, slug=sub_cat)
#     else:
#       category = get_object_or_404(Category, slug=cat, parent_category_id__isnull=True)
#     serializer = self.get_serializer(category)
#     return Response(serializer.data)
  


# class CategoryProductDetailApi(generics.RetrieveAPIView):
#   serializer_class = CategoryProductDetailSerializer
#   lookup_url_kwarg = 'slug'
#   lookup_field = 'slug'

#   def get_queryset(self):
#     return Category.objects.prefetch_related(
#       'products_category_parent_category_id__products_product_category_id'
#     ).select_related('parent_category_id')

#   def get_object(self):
#     queryset = self.get_queryset()
#     obj = get_object_or_404(queryset, **self.kwargs)
#     self.check_object_permissions(self.request, obj)
#     return obj 
  
#   def get_serializer_context(self):
#     context = super().get_serializer_context()
#     products_per_subcat = self.request.query_params.get('products_per_subcat')
#     if products_per_subcat:
#       try:
#         context['products_per_subcat'] = int(products_per_subcat)
#       except ValueError:
#         pass
#     return context
  
#   def retrieve(self, request, *args, **kwargs):
#     instance = self.get_object()
#     serializer = self.get_serializer(instance, context=self.get_serializer_context())
#     return Response(serializer.data, status=status.HTTP_200_OK)
  


class Products(generics.ListAPIView):
  serializer_class = ProductsSerializer
  pagination_class = ProductPagination

  def get_queryset(self):
    query_type = self.request.query_params.get("type", "all")
    qs_map = {
        "best_selling": Product.objects.filter(
            analytics_productrankings_product_id__ranking_type="best_selling",
            analytics_productrankings_product_id__time_period="daily"
        ).order_by(
            "-analytics_productrankings_product_id__rank",
            "-analytics_productrankings_product_id__score",
            "analytics_productrankings_product_id__created_at"
        ),
        "trending": Product.objects.filter(
            analytics_productrankings_product_id__ranking_type="trending",
            analytics_productrankings_product_id__time_period="daily"
        ).order_by(
            "-analytics_productrankings_product_id__rank",
            "-analytics_productrankings_product_id__score",
            "analytics_productrankings_product_id__created_at"
        ),
        "promotions": Product.objects.filter(),  # Adjust filter as needed
        "all": Product.objects.all(),  # FIXED: Changed from .first() to .all() for QuerySet
    }

    qs = qs_map.get(query_type)
    if qs is None:
        # Return empty queryset instead of raising (avoids 500; client handles empty)
        return Product.objects.none()

    return qs

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    query_type = request.query_params.get("type", "all")

    if self.paginator is not None:
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = {
                "total": queryset.count(),  # Your original total (full count)
                "product": serializer.data,  # Paginated results as 'product'
                "type": query_type,
            }
            return self.get_paginated_response(paginated_data)  # Includes count/next/previous

    # Fallback (no pagination)
    serializer = self.get_serializer(queryset, many=True)
    return Response({
        "total": queryset.count(),
        "product": serializer.data,
        "type": query_type,
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


class ProductSearchSuggestionsApi(generics.ListAPIView):
  serializer_class = ProductsSerializer

  def get_queryset(self):
    query = self.request.query_params.get('q', '').strip()
    if not query:
        return Product.objects.none()  # Empty query → empty results

    # Full-text search on name and description (case-insensitive)
    search_qs = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).distinct()

    # FIXED: Order by relevance using Case/When for scoring (exact name match first)
    # Score: 3 for exact prefix match, 2 for contains in name, 1 for description, 0 otherwise
    exact_prefix = f"{query}%"
    search_qs = search_qs.annotate(
        relevance=Case(
            When(name__istartswith=query, then=Value(3)),
            When(name__icontains=query, then=Value(2)),
            When(description__icontains=query, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-relevance', '-created_at')  # High relevance first, then recent

    # Limit to top 4
    return search_qs[:4]
  
  def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    data = {
        'suggestions': response.data,  # Array of 4 product dicts
        'query': request.query_params.get('q', ''),
        'count': len(response.data),
    }


    return Response(data)
  


class ProductSearchApi(generics.ListAPIView):
  """
  API endpoint for full product search results.
  Usage: GET /api/search/?q=search_term&page=1
  Returns paginated products matching the query.
  Supports optional filters: ?category=slug&min_price=0&max_price=100&sort=price (asc/desc)
  Cache: 10 minutes for repeated queries.
  """
  serializer_class = ProductsSerializer
  pagination_class = SearchPagination

  def get_queryset(self):
      query = self.request.query_params.get('q', '').strip()
      if not query:
          return Product.objects.none()

      # Base search on name, description, and tags (extend as needed)
      search_qs = Product.objects.filter(
          Q(name__icontains=query) |
          Q(description__icontains=query), price__gt=0
          # Q(tags__icontains=query)  # Assume tags field
      ).distinct()

      # FIXED: Annotate relevance for ordering (similar to suggestions)
      search_qs = search_qs.annotate(
          relevance=Case(
              When(name__istartswith=query, then=Value(3)),
              When(name__icontains=query, then=Value(2)),
              When(description__icontains=query, then=Value(1)),
              default=Value(0),
              output_field=IntegerField(),
          )
      )

      # Optional filters
      category_slug = self.request.query_params.get('category')
      if category_slug:
          search_qs = search_qs.filter(category__slug=category_slug)

      min_price = self.request.query_params.get('min_price')
      max_price = self.request.query_params.get('max_price')
      if min_price:
          search_qs = search_qs.filter(price__gte=float(min_price))
      if max_price:
          search_qs = search_qs.filter(price__lte=float(max_price))

      # Sorting: ?sort=price (asc), ?sort=-price (desc), ?sort=relevance (default)
      sort = self.request.query_params.get('sort', 'relevance')
      if sort == 'price':
          search_qs = search_qs.order_by('price')
      elif sort == '-price':
          search_qs = search_qs.order_by('-price')
      elif sort == 'relevance':
          search_qs = search_qs.order_by('-relevance', '-created_at')
      else:
          search_qs = search_qs.order_by('-relevance', '-created_at')  # Default fallback

      return search_qs

  def list(self, request, *args, **kwargs):

      response = super().list(request, *args, **kwargs)
      data = {
          'query': request.query_params.get('q', ''),
          'total_results': self.get_queryset().count(),  # Full count for UI progress
          'results': response.data['results'],  # Paginated products
          'filters': {
              'category': request.query_params.get('category'),
              'min_price': request.query_params.get('min_price'),
              'max_price': request.query_params.get('max_price'),
              'sort': request.query_params.get('sort'),
          },
      }
      return Response(data)