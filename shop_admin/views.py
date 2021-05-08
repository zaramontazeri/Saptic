from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from shop import models, serializers
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Subcategory.objects.all()
    serializer_class = serializers.SubcategorySerializer

class ProductsViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer

class ProductVariationViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ProductVariation.objects.all()
    serializer_class = serializers.ProductVariationSerializer
class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer

