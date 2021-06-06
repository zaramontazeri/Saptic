import decimal
from shop.models import Product

from django.db.models import Value
from django.db.models.functions import Coalesce, Least
from django.utils.datetime_safe import date, datetime
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound


class ProductAdminSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=Product
        fields="__all__"


