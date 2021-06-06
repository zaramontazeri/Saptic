from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from shop import models, serializers
from shop_admin import serializers as admin_serializers
from rest_framework.generics import get_object_or_404
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Subcategory.objects.all()
    serializer_class = admin_serializers.SubcategoryAdminSerializer

class ProductsViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Product.objects.all()
    serializer_class = admin_serializers.ProductAdminSerializer
    def list(self,request):
        queryset = models.Product.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.ProductDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ProductDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductVariationViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ProductVariation.objects.all()
    serializer_class = admin_serializers.VariationAdminSerializer
class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer

class ProductAttributeViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ProductAttribute.objects.all()
    serializer_class = serializers.ProductAttributeSerializer

class FrameColorViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.FrameColor.objects.all()
    serializer_class = serializers.FrameColorSerializer

class ProductVariationShopViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ProductVariationShop.objects.all()
    serializer_class = serializers.ProductVariationShopSerializer
class WalletViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Wallet.objects.all()
    serializer_class = serializers.WalletSerializer

class WalletProductCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = admin_serializers.ProductWalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

