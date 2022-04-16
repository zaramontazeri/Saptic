from shop.models import ChargeTransaction
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CategoryListAPIView,
                    ProductsListAPIView,
                    ProductsCategoryListAPIView,
                    ProductDetailView,
                    InvoiceView,
                    DiscountCheck,
                    TestInPlaceView,
                    SubcategoryListAPIView, UserWalletsInfoList, WalletCharge
                    )
# OrderedItemViewSet

# router = DefaultRouter()
# router.register(r'ordereditem', OrderedItemViewSet)
# urlpatterns = router.urls
# urlpatterns = +[
urlpatterns = [
    path('categories/', CategoryListAPIView.as_view()),
    path('products/<int:c_id>/', ProductsCategoryListAPIView.as_view(), name='products_category'),
    path('products/', ProductsListAPIView.as_view(), name='products'),
    path('product_detail/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path("discount_check/", DiscountCheck.as_view(),name="discount_check"),
    path('invoice/', InvoiceView.as_view(), name='invoice'),
    path('test_in_place/', TestInPlaceView.as_view(), name='test_in_place'),
    path('subcategories/<int:c_id>/', SubcategoryListAPIView.as_view(), name='subcategories'),
    path('user_wallet_list/', UserWalletsInfoList.as_view(), name='user_wallet'),
    path('charge/', WalletCharge.as_view(), name='charge'),
]
