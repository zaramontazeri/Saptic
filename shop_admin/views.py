from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from shop import models, serializers
from shop_admin import serializers as admin_serializers
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Subcategory.objects.all()
    serializer_class = serializers.SubcategoryAdminSerializer

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
# class ProductVariationViewSet(viewsets.ModelViewSet):
#     """ViewSet for the OrderItem class"""
#     queryset = models.ProductVariation.objects.all()
#     serializer_class = serializers.ProductVariationSerializer
class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer

