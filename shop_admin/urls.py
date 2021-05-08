from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,ShopViewSet,SubCategoryViewSet,ProductsViewSet,ProductVariationViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'subcategory', SubCategoryViewSet)

router.register(r'shop', ShopViewSet)
router.register(r'product', ProductsViewSet)
# router.register(r'variation', ProductVariationViewSet)

urlpatterns = router.urls
# urlpatterns = +[
urlpatterns += [
]
