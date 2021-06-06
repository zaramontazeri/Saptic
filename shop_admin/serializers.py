import decimal
from functools import update_wrapper
from shop.serializers import ChoiceSerializer, FrameColorSerializer, GlassColorSerializer, ProductAttributeSerializer, ProductChoiceSerializer, ProductGalleryImageSerializer, ProductVariationAttributeSerializer
from shop.models import Choices, Product, ProductVariation, Subcategory, Wallet

from django.db.models import Value
from django.db.models.functions import Coalesce, Least
from django.utils.datetime_safe import date, datetime
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound


class ProductAdminSerializer(serializers.ModelSerializer):
    product_images=ProductGalleryImageSerializer(many=True) #if I wanted to use other name I had to use source=product_images

    class Meta:
        model=Product
        fields="__all__"
    def create(self, validated_data):
        product_images = validated_data.pop('product_images')
        variation = ProductVariation.objects.create(**validated_data)
        self.create_product_images(variation,product_images)
        return variation
         
    def create_product_images(self,instance,product_images):
        for choice in product_images:
            choice["prduct"]= instance.id
            serializer = ProductGalleryImageSerializer(data=choice)
            if serializer.is_valid():
                serializer.save()           
        return
    def update(self, instance, validated_data):
        product_images = validated_data.pop('product_images')
        self.update_product_images(instance,product_images)
        for field in validated_data:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance
    def update_product_images(self,instance,_data):
        remove_items = { item.id: item for item in instance.product_images.all() }
        for item in _data:
            item_id = item.get("id", None)
            if item_id is None:
                # new item so create this
                item["product"]= instance.id
                serializer = ProductGalleryImageSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()    
            elif remove_items.get(item_id, None) is not None:
                # update this item
                instance_item = remove_items.pop(item_id)
                serializer = ProductGalleryImageSerializer(instance_item, data=item)
                if serializer.is_valid():
                    serializer.save()
        for item in remove_items.values():
            item.delete()
        return
class SubcategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class VariationAdminSerializer(serializers.ModelSerializer):
    # specifications=ProductAttributeSerializer(many=True,read_only=True)
    specifications=ProductVariationAttributeSerializer(source='productvariationattribute_set', many=True)
    product_choices = ProductChoiceSerializer(source="product_choices",many=True)
    glasses = GlassColorSerializer(source ="glasses",many=True)
    color=FrameColorSerializer()
    #IT IS IMPORTANT TO USE RELATED_NAME in models AND SOURCE in serializer . beCuz Calling the serializer for a ManyToManyField only works on the end point (i.e. ProductAttribute in this case).
    #link: 1-problem:https://www.reddit.com/r/django/comments/6yrh9k/drf_serialization_not_working_on_many_to_many/
    #link: solution:https://www.reddit.com/r/django/comments/6yrh9k/drf_serialization_not_working_on_many_to_many/dms01dv/
    occasional_discount=serializers.StringRelatedField()
    # discount_price=serializers.ReadOnlyField()
    class Meta:
        model = ProductVariation
        fields =["id","title_size","price","discount_price","occasional_discount","specifications","created_at","updated_at",'color','product_choices']
    
    def create(self, validated_data):

        product_choices = validated_data.pop('product_choices')
        specifications = validated_data.pop("specifications")
        glasses = validated_data.pop("glasses")

        variation = ProductVariation.objects.create(**validated_data)
        self.create_product_choice(variation,product_choices)
        self.create_specifications(variation,specifications)
        self.create_glasses(variation ,glasses)
        return variation
    def create_product_choice(self,instance,product_choices):
        for choice in product_choices:
            choice["prduct_variation"]= instance.id
            serializer = ChoiceSerializer(data=choice)
            if serializer.is_valid():
                serializer.save()           
        return 
    def create_specifications(self,instance,specifications):
        for item in specifications:
            item["product_variation"]= instance.id
            serializer = ProductVariationAttributeSerializer(data=item)
            if serializer.is_valid():
                serializer.save()           
        return 
    def create_glasses(self,instance,glasses):
        for item in glasses:
            item["product_variation"]= instance.id
            serializer = ProductVariationAttributeSerializer(data=item)
            if serializer.is_valid():
                serializer.save()           
        return 
    def update(self, instance, validated_data):
        product_choices = validated_data.pop('product_choices')
        specifications = validated_data.pop("specifications")
        glasses = validated_data.pop("glasses")
        self.update_product_choice(instance,product_choices)
        self.update_specifications(instance,specifications)
        self.update_glasses(instance,glasses)
        for field in validated_data:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        instance.save()
        return instance
    def update_product_choice(self,instance,_data):
        remove_items = { item.id: item for item in instance.product_choices.all() }
        for item in _data:
            item_id = item.get("id", None)
            if item_id is None:
                # new item so create this
                item["product_variation"]= instance.id
                serializer = ProductChoiceSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()    
            elif remove_items.get(item_id, None) is not None:
                # update this item
                instance_item = remove_items.pop(item_id)
                serializer = ProductChoiceSerializer(instance_item, data=item)
                if serializer.is_valid():
                    serializer.save()
        for item in remove_items.values():
            item.delete()
        return
    def update_specifications(self,instance,_data):
        remove_items = { item.id: item for item in instance.specifications.all() }
        for item in _data:
            item_id = item.get("id", None)
            if item_id is None:
                # new item so create this
                item["product_variation"]= instance.id
                serializer = ProductAttributeSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()    
            elif remove_items.get(item_id, None) is not None:
                # update this item
                instance_item = remove_items.pop(item_id)
                serializer = ProductAttributeSerializer(instance_item, data=item)
                if serializer.is_valid():
                    serializer.save()
        for item in remove_items.values():
            item.delete()
        return
    def update_glasses(self,instance,_data):
        remove_items = { item.id: item for item in instance.glasses.all() }
        for item in _data:
            item_id = item.get("id", None)
            if item_id is None:
                # new item so create this
                item["product_variation"]= instance.id
                serializer = GlassColorSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()    
            elif remove_items.get(item_id, None) is not None:
                # update this item
                instance_item = remove_items.pop(item_id)
                serializer = GlassColorSerializer(instance_item, data=item)
                if serializer.is_valid():
                    serializer.save()
        for item in remove_items.values():
            item.delete()
        return

class ProductWalletSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        wallet_id = serializers.IntegerField()
        def create(self,validated_data):
            product = Product.objects.get(id=validated_data["product_id"])
            wallet = Wallet.objects.get(id=validated_data['wallet_id'])
            wallet.products.add(product)
            return wallet            