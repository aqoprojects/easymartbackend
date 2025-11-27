from django.urls import path
from accounts import views as CustomerViews
from products import views as ProdcutViews
from promotions import views as PromotionViews
from orders import views as OrderViews
from cart import views as CartViews
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView
)

urlpatterns = [
  path('register/', CustomerViews.customerRegisterationView.as_view()),
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

  path('categories/', ProdcutViews.ProductCategories.as_view(), name='categories'),
  path('products/', ProdcutViews.Products.as_view(), name='products'),
  path('product/<slug:product_slug>/', ProdcutViews.ProductAPI.as_view(), name="product"),

  path('promotions/', PromotionViews.Promotion.as_view(), name="promotions"), 

  path('carts/', CartViews.CartApi.as_view(), name="carts"),
  path('add_cart/', CartViews.CartCreateApi.as_view(), name="cartItems"),
  path('update_cart/<slug:cart_item_id>/', CartViews.CartUpdateApi.as_view(), name="update_cartItems"),
  path('delete_cart/<slug:cart_item_id>/', CartViews.CartDeleteApi.as_view(), name="delete_cartItems"),


  path('orders/', OrderViews.OrdersApi.as_view(), name="orders"),


]