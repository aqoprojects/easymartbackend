from django.urls import path
from accounts import views as CustomerViews
from products import views as ProdcutViews
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
  path('product/<slug:product_slug>/', ProdcutViews.Product.as_view(), name="product"),
]