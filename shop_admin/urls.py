from pages.models import PageContent
from shop.models import ProductAttribute
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AssignProductToBoxAPIView, CategoryViewSet, DepotViewSet, DiscountCodeViewSet, \
    FrameColorViewSet, NProductInstanceCreateAPIView, OccasionalDiscountViewSet, ProductAttributeChoiceViewSet, ProductAttributeViewSet, ProductBoxTransferListAPIView, \
    ProductBoxTransferRetrieveUpdateDestroyAPIView, ProductBoxViewSet, ProductInstanceViewSet, ProductVariationShopViewSet, \
    ProductVariationViewSet, PromotionalCodeViewSet, SendProductBoxesTo, ShopRequestViewSet, ShopUserCreateView, ShopUserListView, ShopUserRetrieveUpdateDestroyView,\
    ShopViewSet,SubCategoryViewSet,ProductsViewSet, VariationGlassChoiceRetrieveAPIView, WalletProductCreateView, WalletViewSet,NProductBoxCreateAPIView,\
       PageContentViewSet 
# ,ProductVariationViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'subcategory', SubCategoryViewSet)
router.register(r'shop', ShopViewSet)
router.register(r'product', ProductsViewSet)
router.register(r'variation', ProductVariationViewSet)
router.register(r'attribute', ProductAttributeViewSet)
router.register(r'choice_attribute', ProductAttributeChoiceViewSet)
router.register(r'frame_color', FrameColorViewSet)
router.register(r'product_shop', ProductVariationShopViewSet)
router.register(r'wallet', WalletViewSet)
router.register(r'productbox', ProductBoxViewSet)
router.register(r'productinstance', ProductInstanceViewSet)
router.register(r'depot', DepotViewSet)
router.register(r'shoprequest', ShopRequestViewSet)
router.register(r'pagecontent', PageContentViewSet)
router.register(r'discount', DiscountCodeViewSet)
router.register(r'promotional', PromotionalCodeViewSet)
router.register(r'ocational', OccasionalDiscountViewSet)

urlpatterns = router.urls
# urlpatterns = +[
urlpatterns += [
    path('wallet_product/', WalletProductCreateView.as_view(), name='walletproduct'),
    path('shop_users/', ShopUserListView.as_view(), name='shop_users'),
    path('shop_users/create/', ShopUserCreateView.as_view(), name='shop_users'),
    path('shop_users/<int:pk>/', ShopUserRetrieveUpdateDestroyView.as_view(), name='shop_users'),
    path('nproductinstance/', NProductInstanceCreateAPIView.as_view(), name='n_product_instance'),
    path('nproductbox/', NProductBoxCreateAPIView.as_view(), name='n_product_box'),
    path('assign_products_to_box/', AssignProductToBoxAPIView.as_view(), name='n_product_box'),
    path('send_productbox_to/', SendProductBoxesTo.as_view(), name='send_product_to'),
    
    path('boxtransfer/', ProductBoxTransferListAPIView.as_view(), name='box_transfer_list'),
    path('boxtransfer/<int:pk>/', ProductBoxTransferRetrieveUpdateDestroyAPIView.as_view(), name='box_transfer_retrieve_update_destroy'),
    path('var_glass_choice/<int:pk>/', VariationGlassChoiceRetrieveAPIView.as_view(), name='box_transfer_retrieve_update_destroy'),

]
