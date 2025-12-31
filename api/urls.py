from django.urls import path
from accounts import views as CustomerViews
from products import views as ProdcutViews
from promotions import views as PromotionViews
from orders import views as OrderViews
from cart import views as CartViews
from django.urls import re_path

urlpatterns = [
  path('register/', CustomerViews.customerRegisterationView.as_view()),
  path('auth/login/', CustomerViews.LoginView.as_view()),
  path('auth/logout/', CustomerViews.LogoutView.as_view()),
  path('auth/refresh/', CustomerViews.TokenRefreshView.as_view(), name='token_refresh'),
  path('auth/me/', CustomerViews.ProfileView.as_view(), name='customer_profile'),

  path('categories/', ProdcutViews.TopLevelCategoryListView.as_view(), name='category-list'),
  path('categories/<slug:pk>/', ProdcutViews.CategoryDetailView.as_view(), name='category-detail'),
  path('categories/<slug:pk>/children/', ProdcutViews.CategoryChildrenListView.as_view(), name='category-children'),
  path('categories/<uuid:pk>/products/', ProdcutViews.CategoryProductsListView.as_view(), name='category-products'),
  # path('refresh/', CustomerViews.TokenRefreshView.as_view(), name='token_refresh'),

  # path('categories/', ProdcutViews.CategoriesApi.as_view(), name='categories'),
  # path('category/<slug:cat>/subcats/', ProdcutViews.SubCategoryApi.as_view(), name='sub_categories'),
  # re_path(r'^category/(?P<cat>[-a-zA-Z0-9_]+)(/(?P<sub_cat>[-a-zA-Z0-9_]+))?/$', ProdcutViews.ProductSubCategories.as_view(), name='product_category'),
  # path('category/<slug:cat>/<slug:sub_cat>/', ProdcutViews.ProductSubCategories.as_view(), name='product_category'),
  path('products/', ProdcutViews.Products.as_view(), name='products'),
  path('product/<slug:product_slug>/', ProdcutViews.ProductAPI.as_view(), name="product"),
  path('search/suggest/', ProdcutViews.ProductSearchSuggestionsApi.as_view(), name="product_search"), 
  path('search/', ProdcutViews.ProductSearchApi.as_view(), name="product_search"),

  path('promotions/', PromotionViews.Promotion.as_view(), name="promotions"), 

  path('carts/', CartViews.CartApi.as_view(), name="carts"),
  path('add_cart/', CartViews.CartCreateApi.as_view(), name="cartItems"),
  path('update_cart/<slug:cart_item_id>/', CartViews.CartUpdateApi.as_view(), name="update_cartItems"),
  path('delete_cart/<slug:cart_item_id>/', CartViews.CartDeleteApi.as_view(), name="delete_cartItems"),


  path('orders/', OrderViews.OrdersApi.as_view(), name="orders"),


  path('checkout/', CartViews.create_checkout_session.as_view()),
  path('webhook/', CartViews.StripeWebhookView.as_view(), name="webhook")


]