from django.urls import path
from demo.views.ProductViews import ProductListAPIView, CreateProductAPIView

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/create/", CreateProductAPIView.as_view(), name="product-create"),
]
