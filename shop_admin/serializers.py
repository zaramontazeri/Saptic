from domains.serializers import DomainSerializer
from domains.models import Domain
from auth_rest_phone.serializers import UserSerializer
import decimal
from functools import update_wrapper
from django.contrib.auth import get_user_model

from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from media_app.serializers import FileRelatedField, FileSmallSerializer
from shop.serializers import CategorySerializer, ChoiceSerializer,\
FrameColorSerializer, GlassColorSerializer,\
 ProductAttributeSerializer, ProductChoiceSerializer, ProductDetailSerializer,\
  ProductGalleryImageSerializer, ShopSerializer, WorkingTimeSerilizer
from shop.models import Category, ChoiceAttribute, Choices, Depot, DiscountCode, FrameColor, GlassColor, OccasionalDiscount, Product, ProductAttribute, ProductBox, ProductInstance, ProductVariation, PromotionalCode, Shop, Subcategory, Wallet

from django.db.models import Value
from django.db.models.functions import Coalesce, Least
from django.utils.datetime_safe import date, datetime
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

User = get_user_model()

class FrameColorRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return FrameColor.objects.all()

    def to_representation(self, instance):
        request  = self.context.get('request', None)
        if request:
            image = FileSmallSerializer(instance.image,context={"request":request}).data
            return {
                "id":instance.id,
                "image":image,
                "color_name":instance.color_name
             }
        else :
            image = FileSmallSerializer(instance.image,contect={"request":request}).data
            return {
                "image":image,
                "color_name":instance.color_name
             }

    def to_internal_value(self, data):
        # name = data.get('name', None)
        # inventor = data.get('inventor', None)
        id = data
        if not isinstance(data ,FrameColor):
            return FrameColor.objects.get(pk=id)
        else :
            return data
class ProductAdminSerializer(WritableNestedModelSerializer):
    subcategory_detail = serializers.SerializerMethodField()
    
    class Meta:
        model=Product
        exclude=["related_products"]
    def get_subcategory_detail(self,instance):
        return SubcategoryAdminSerializer(instance.subcategory).data
    # def create(self, validated_data):
    #     product_images = validated_data.pop('product_images')
    #     variation = Product.objects.create(**validated_data)
    #     self.create_product_images(variation,product_images)
    #     return variation
         
    # def create_product_images(self,instance,product_images):
    #     context = {}
    #     context["product"]= instance
    #     context["request"]= self.context.get("request",None)
    #     for choice in product_images:

    #         serializer = ProductGalleryImageSerializer(data=choice,context=context)
    #         if serializer.is_valid():
    #             serializer.save()           
    #     return
    # def update(self, instance, validated_data):
    #     product_images = validated_data.pop('product_images')
    #     self.update_product_images(instance,product_images)
    #     for field in validated_data:
    #         setattr(instance, field, validated_data.get(field, getattr(instance, field)))
    #     instance.save()
    #     return instance
    # def update_product_images(self,instance,_data):
    #     remove_items = { item.id: item for item in instance.product_images.all() }
    #     context = {}
    #     context["product"]= instance
    #     context["request"]= self.context.get("request",None)
    #     for item in _data:
    #         item_id = item.get("id", None)
    #         if item_id is None:
                
    #             # new item so create this
    #             serializer = ProductGalleryImageSerializer(data=item,context=context)
    #             if serializer.is_valid():
    #                 serializer.save()    
    #         elif remove_items.get(item_id, None) is not None:
    #             # update this item
    #             instance_item = remove_items.pop(item_id)
    #             serializer = ProductGalleryImageSerializer(instance_item, data=item,context=context)
    #             if serializer.is_valid():
    #                 serializer.save()
    #     for item in remove_items.values():
    #         item.delete()
    #     return

class SubcategoryAdminSerializer(serializers.ModelSerializer):
    cover =FileRelatedField()
    category = PresentablePrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        presentation_serializer=CategorySerializer,
        read_source=None,
    )
    class Meta:
        model = Subcategory
        fields = '__all__'

class ChoiceAttributeAdminSerializer(WritableNestedModelSerializer):
    attribute =  PresentablePrimaryKeyRelatedField(
        queryset=ProductAttribute.objects.all(),
        presentation_serializer=ProductAttributeSerializer,
        read_source=None,
    )
    class Meta:
        model=ChoiceAttribute
        fields ='__all__'   


class VariationAdminSerializer(WritableNestedModelSerializer):
    specifications=  PresentablePrimaryKeyRelatedField(
        queryset=ChoiceAttribute.objects.all(),
        presentation_serializer=ChoiceAttributeAdminSerializer,
        many=True,
        required=False
    )
  
    product_choices = ProductChoiceSerializer(many=True)
    product = PresentablePrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        presentation_serializer=ProductDetailSerializer,
        read_source=None,
    )
    glasses = GlassColorSerializer(many=True)
    color=FrameColorRelatedField()
    cover = FileRelatedField()
    occasional_discount=serializers.StringRelatedField()
    product_variations_images=ProductGalleryImageSerializer(many=True)
    #  PresentablePrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     presentation_serializer=UserSerializer,

    #     read_source=None,
    #     many=True
    # )
    cover = FileRelatedField()
    class Meta:
        model = ProductVariation
        fields =["id",'slug',"title_size","price","discount_price","occasional_discount","specifications","created_at","updated_at",'color','product_choices','glasses','product','cover','product_variations_images']
        
 
class VariationGlassChoiceAdminSerializer(WritableNestedModelSerializer):
    product_choices = ProductChoiceSerializer(many=True)
    glasses = GlassColorSerializer(many=True)
    class Meta:
        model = ProductVariation
        fields =["id",'slug','product_choices','glasses']
        

class ProductWalletSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        wallet_id = serializers.IntegerField()
        
        def create(self,validated_data):
            product = Product.objects.get(id=validated_data["product_id"])
            wallet = Wallet.objects.get(id=validated_data['wallet_id'])
            wallet.products.add(product)
            return wallet          
        
class ShopCreateSerializer(UniqueFieldsMixin,WritableNestedModelSerializer):
    working_times=WorkingTimeSerilizer(many=True)
    cover = FileRelatedField()
    domain = DomainSerializer()
    owner =  PresentablePrimaryKeyRelatedField(
        queryset=User.objects.all(),
        presentation_serializer=UserSerializer,
        read_source=None,
        many=True,
    )
    class Meta:
        model= Shop
        fields = '__all__'

class ProductInstanceSerializer(serializers.ModelSerializer):

    glass_color = PresentablePrimaryKeyRelatedField(
        queryset=GlassColor.objects.all(),
        presentation_serializer=GlassColorSerializer,
        read_source=None,
    )
    choices = PresentablePrimaryKeyRelatedField(
        queryset=Choices.objects.all(),
        presentation_serializer=ChoiceSerializer,
        read_source=None,
        many=True
    )

    sold_out = PresentablePrimaryKeyRelatedField(
        queryset=Shop.objects.all(),
        presentation_serializer=ShopSerializer,
        read_source=None,
        required=False
    )

    # product_variation = PresentablePrimaryKeyRelatedField(
    #     queryset=ProductVariation.objects.all(),
    #     presentation_serializer=ProductVar,
    #     read_source=None,
    # )
    class Meta:
        model = ProductInstance
        fields = "__all__" 

class ProductBoxSerializer(serializers.ModelSerializer):
    empty_size = serializers.SerializerMethodField()
    productinstances = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = ProductBox
        fields = "__all__" 
    def get_empty_size(self,obj):
        count_inbox = obj.count_in_box
        instance_inbox =len (obj.productinstances.all())
        return count_inbox - instance_inbox 



class DepotSerializer(serializers.ModelSerializer):
    owner =  PresentablePrimaryKeyRelatedField(
        queryset=User.objects.all(),
        presentation_serializer=UserSerializer,
        read_source=None,
        many=True,
        required=False
    )
    class Meta:
        model = Depot
        fields = "__all__" 


class PromotionalCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionalCode
        fields = "__all__" 
class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = "__all__" 
class OccasionalDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccasionalDiscount
        fields = "__all__" 