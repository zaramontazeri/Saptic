from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CategoryListAPIView,
                    ProductsListAPIView,
                    MenuItemListAPIView,
                    ProductsCategoryListAPIView,
                    ProductDetailView,
                    InvoiceDetailView,
                    DiscountCheck)
# OrderedItemViewSet

# router = DefaultRouter()
# router.register(r'ordereditem', OrderedItemViewSet)
# urlpatterns = router.urls
# urlpatterns = +[
urlpatterns = [
    path('categories/', CategoryListAPIView.as_view()),
    path('products/<int:c_id>/', ProductsCategoryListAPIView.as_view(), name='products_category'),
    path('products/', ProductsListAPIView.as_view(), name='products'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path("discount_check/", DiscountCheck.as_view(),name="discount_check"),
    path('invoice/', InvoiceView.as_view(), name='products'),
    path('subcategories/<int:c_id>/', MenuItemListAPIView.as_view(), name='subcategories'),
]
