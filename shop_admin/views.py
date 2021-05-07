from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from shop import models, serializers
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

