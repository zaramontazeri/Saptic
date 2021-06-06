from shop.models import ProductAttribute
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FrameColorViewSet, ProductAttributeViewSet, ProductVariationShopViewSet, ProductVariationViewSet,ShopViewSet,SubCategoryViewSet,ProductsViewSet, WalletProductCreateView, WalletViewSet
# ,ProductVariationViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'subcategory', SubCategoryViewSet)
router.register(r'shop', ShopViewSet)
router.register(r'product', ProductsViewSet)
router.register(r'variation', ProductVariationViewSet)
router.register(r'attribute', ProductAttributeViewSet)
router.register(r'frame_color', FrameColorViewSet)
router.register(r'product_shop', ProductVariationShopViewSet)
router.register(r'wallet', WalletViewSet)

urlpatterns = router.urls
# urlpatterns = +[
urlpatterns += [
    path('wallet_product/', WalletProductCreateView.as_view(), name='walletproduct'),
]
