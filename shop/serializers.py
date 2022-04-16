from django.contrib.auth import get_user_model
from drf_writable_nested.serializers import WritableNestedModelSerializer
from auth_rest_phone.serializers import UserSerializer
import decimal
from media_app.serializers import FileRelatedField, FileSerializer, FileSmallSerializer
from rest_framework import validators
from django.db.models import Value, fields
from django.db.models.functions import Coalesce, Least
from django.utils.datetime_safe import date, datetime
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound
from shop.models import ChoiceAttribute, Choices, FrameColor, GlassColor, ProductChoice,\
ProductVariationShop, Shop, Product,\
ProductVariation, ProductVariationAttribute, ProductAttribute, \
ProductGalleryImage, ProductReview, DiscountCode, PromotionalCode, ShopRequest, \
UserWallet, Wallet,WorkingTime,OrderedItem,\
Transactions,Invoice,TestInPlace,Category,Subcategory
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
User = get_user_model()

class VideoField(serializers.Field):
    def to_representation(self, value):
        my_video = detect_backend(value)
        res = {}
        try:
            res['info'] = my_video.get_info()
        except :
            pass
        try:
            res['code'] = my_video.get_code()
        except :
            pass
        try:
            res["url"] = my_video.get_url()
        except :
            pass
        # try:
        #     res["thumbnail"] = my_video.get_thumbnail_url()
        # except :
        #     pass

        return res

class ProductAttributeRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return ProductAttribute.objects.all()

    def to_representation(self, instance):
        return {
            'id':instance.id,
            'title':instance.title
        }

    def to_internal_value(self, data):
        # name = data.get('name', None)
        # inventor = data.get('inventor', None)
        id = data
        if not isinstance(data ,ProductAttribute):
            return ProductAttribute.objects.get(pk=id)
        else :
            return data


class WorkingTimeSerilizer(serializers.ModelSerializer):
    day_of_week = serializers.SerializerMethodField()
    
    class Meta:
        model= WorkingTime
        exclude =["branch"]        
    def get_day_of_week (self,instance):
        days = {
            "1":"شنبه",
            "2":"یک شنبه",
            "3":"دو شنبه",
            "4":"سه شنبه",
            "5":"چهارشنبه",
            "6":"پنج شنبه",
            "7":"جمعه"
        }
        return days[instance.day]
    def create(self, validated_data):
        p =WorkingTime.objects.create(**validated_data)
        return p
class ShopSerializer(serializers.ModelSerializer):
    working_times=WorkingTimeSerilizer(many=True)
    cover = FileRelatedField()
    domain = serializers.StringRelatedField()
    owner =  PresentablePrimaryKeyRelatedField(
        queryset=User.objects.all(),
        presentation_serializer=UserSerializer,

        read_source=None
    )
    class Meta:
        model= Shop
        fields = '__all__'
    def create(self, validated_data):
        working_times = validated_data.pop('working_times')
        # framecolor = FrameColor.
        shop = Shop.objects.create(**validated_data)
        context = {}
        context["shop"]= shop
        context["request"]= self.context.get("request",None)
        for times in working_times:
            serializer = WorkingTimeSerilizer(data=times,context=context)
            if serializer.is_valid(raise_exception=True):
                serializer.save()            
        result = ProductVariation.objects.get(pk=shop.id)

        return result

class CategorySerializer(serializers.ModelSerializer):
    cover_image = FileRelatedField()

    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    cover =FileRelatedField()
    class Meta:
        model = Subcategory
        fields = '__all__'

###PRODUCT LIST
##############MANY2MANY WITH THROUGH  NESTED SERIALIZER#################################################
class ProductAttributeSerializer1(serializers.ModelSerializer):
    class Meta:
        model=ProductAttribute
        fields ='__all__'

class ChoiceAttributeSerializer(serializers.ModelSerializer):
    attribute =  PresentablePrimaryKeyRelatedField(
        queryset=ProductAttribute.objects.all(),
        presentation_serializer=ProductAttributeSerializer1,
        read_source=None,
    )
    class Meta:
        model=ChoiceAttribute
        fields ='__all__'   

class ProductAttributeSerializer(serializers.ModelSerializer):
    choices = ChoiceAttributeSerializer(many=True,read_only=True)
    class Meta:
        model=ProductAttribute
        fields ='__all__'



class ProductVariationShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVariationShop
        fields ='__all__'

# class ProductVariationAttributeSerializer(WritableNestedModelSerializer):
#     choice_attribute = PresentablePrimaryKeyRelatedField(queryset=ChoiceAttribute.objects.all(),
#         presentation_serializer=ChoiceAttributeSerializer,
#         read_source=None,
#         required = False
#     )
#     attribute = PresentablePrimaryKeyRelatedField(queryset=ProductAttribute.objects.all(),
#         presentation_serializer=ProductAttributeSerializer,
#         read_source=None,
#         required = False
#     )
#     class Meta:
#         model=ProductVariationAttribute
#         exclude =["product_variation"]        

class FrameColorSerializer(serializers.ModelSerializer):
    image = FileRelatedField()
    class Meta:
        model=FrameColor
        fields = '__all__'

class GlassColorSerializer(serializers.ModelSerializer):
    image = FileRelatedField()
    class Meta:
        model=GlassColor
        # fields = '__all__'
        exclude =["product_variation"]        
    def create(self, validated_data):
        # glass =GlassColor.objects.create(**validated_data,product_variation=self.context.get("product_variation"))
        glass =GlassColor.objects.create(**validated_data)

        return glass    

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choices
        exclude =["product_choice"]        
    def create(self, validated_data):
        choice =Choices.objects.create(**validated_data)
        return choice  

class ProductChoiceSerializer(WritableNestedModelSerializer):
    choices = ChoiceSerializer(many=True)
    class Meta:
        model=ProductChoice
        exclude =["product_variation"]        

    # def create(self, validated_data):
    #     choices_data = validated_data.pop('choices')
    #     # product_choice = ProductChoice.objects.create(**validated_data,product_variation=self.context.get("product_variation"))
    #     product_choice = ProductChoice.objects.create(**validated_data)

    #     context = {}
    #     context["product_choice"]= product_choice
    #     context["request"]= self.context.get("request",None)
    #     for choice in choices_data:
    #         serializer = ChoiceSerializer(data=choice,context=context)
    #         if serializer.is_valid():
    #             serializer.save()           
    #     return product_choice
    # def update(self, instance, validated_data):
    #     _data = validated_data.pop("choices")
    #     remove_items = { item.id: item for item in instance.choices.all() }
    #     context = {}
    #     context["product"]= instance
    #     context["request"]= self.context.get("request",None)
    #     for item in _data:
    #         item_id = item.get("id", None)

    #         if item_id is None:
    #             # new item so create this
    #             serializer = ChoiceSerializer(data=item,context=context)
    #             if serializer.is_valid():
    #                 serializer.save()    
    #         elif remove_items.get(item_id, None) is not None:
    #             # update this item
    #             instance_item = remove_items.pop(item_id)
    #             serializer = ChoiceSerializer(instance_item, data=item,context=context)
    #             if serializer.is_valid():
    #                 serializer.save()
    #     for item in remove_items.values():
    #         item.delete()
    #     for field in validated_data:
    #         setattr(instance, field, validated_data.get(field, getattr(instance, field)))
    #     instance.save()
    #     return instance
class ProductGalleryImageSerializer(serializers.ModelSerializer):
    image = FileRelatedField()
    class Meta:
        model=ProductGalleryImage
        exclude =["product"]        
    def create(self, validated_data):
        p =ProductGalleryImage.objects.create(**validated_data)
        return p
class VariationPriceSerializer(serializers.ModelSerializer):
    # specifications=ProductAttributeSerializer(many=True,read_only=True)
    specifications=ChoiceAttributeSerializer( many=True)
    color=FrameColorSerializer()
    cover = FileRelatedField()
    glasses = GlassColorSerializer(many=True)
    product_variations_images= ProductGalleryImageSerializer(many=True)
    #IT IS IMPORTANT TO USE RELATED_NAME in models AND SOURCE in serializer . beCuz Calling the serializer for a ManyToManyField only works on the end point (i.e. ProductAttribute in this case).
    #link: 1-problem:https://www.reddit.com/r/django/comments/6yrh9k/drf_serialization_not_working_on_many_to_many/
    #link: solution:https://www.reddit.com/r/django/comments/6yrh9k/drf_serialization_not_working_on_many_to_many/dms01dv/
    occasional_discount=serializers.StringRelatedField()
    product_choices = ProductChoiceSerializer(many=True)
    # discount_price=serializers.ReadOnlyField()
    class Meta:
        model = ProductVariation
        fields =["id","title_size",'slug',"price","discount_price","occasional_discount","specifications","created_at","updated_at",'color','glasses',"product_variations_images","cover",'product_choices']



class ProductListSerializer(serializers.ModelSerializer):
    #todo u need to add star rating later
    variations = serializers.SerializerMethodField()
    video = VideoField()
    cover = FileRelatedField()

    class Meta:
        model=Product
        fields = ['id','cover','title','variations','video', "content",'slug']
        read_only_fields=["id"]
    def get_variations(self,instance):
        # today = date.today()
        # today_str = datetime.today().strftime("%A")
        # Query = Q(variations__special_dates__start_date__gte=today) | Q(
        #     variations__special_dates__end_date__gte=today) | Q(variations__special_dates__day=today_str.lower())
        variations = instance.variations.all().annotate(final_price=Least("price",Coalesce("discount_price", Value(100000000000)))).order_by("final_price")

        # for variation in variations.all():
        #     print(variation.final_price)
        #variations = instance.variations.all()

        return VariationPriceSerializer(variations,many=True).data

################### PRODUCT DETAIL####################

class RelatedProductSerializer(serializers.ModelSerializer):
    variations_best_price=serializers.SerializerMethodField()
    variations_info=serializers.SerializerMethodField()
    
    class Meta:
        model=Product
        fields = ['id','title','variations_best_price','variations_info','slug']

    def get_variations_best_price(self,instance):
        variations = instance.variations.all().annotate(
            final_price=Least("price", Coalesce("discount_price", Value(100000000000)))).order_by("final_price")
        best_price = None
        if len(variations) > 0:
            best_price = variations[0].final_price
        return str(best_price)
    def get_variations_info(self,instance):
        colors = self.context.get('colors',None)
        if colors :
            variations = instance.variations.filter(color__slug__in=colors)
        else:
            variations = instance.variations.all()
        results= []
        for variation in variations:
            result = {}
            result["id"]=variation.id
            result["slug"] = variation.slug
            result["color"]=FrameColorSerializer(variation.color,context={"request":self.context["request"]}).data
            result["cover"]=FileSmallSerializer(variation.cover,context={"request":self.context["request"]}).data
            variation_images =variation.product_variations_images.all()
            result["product_choices"] = ProductChoiceSerializer(variation.product_choices.all(),many=True).data
            result["product_variations_images"] = []
            for variation_image in variation_images:
                result["product_variations_images"].append(ProductGalleryImageSerializer(variation_image,context={"request":self.context["request"]}).data)
            results.append(result)
        return results  


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductReview
        exclude=["product"]

class WalletSerializer(serializers.ModelSerializer):
    products=serializers.StringRelatedField()
    cover = FileRelatedField()
    class Meta:
        model = Wallet
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    # product_images=ProductGalleryImageSerializer(many=True) #if I wanted to use other name I had to use source=product_images
    variations=VariationPriceSerializer(many=True)
    related_products=RelatedProductSerializer(many=True)
    product_reviews=serializers.SerializerMethodField()
    wallet_to_product =WalletSerializer(many=True)
    # cover = FileRelatedField()
    subcategory_detail = serializers.SerializerMethodField()
    # attributes = ProductAttributeSerializer(many=True)
    
    class Meta:
        model=Product
        fields="__all__"
    def get_product_reviews(self,instance):
        # query=ProductReview.objects.filter(product=instance,confirmed=True) this is equal to next line
        query_set= instance.product_reviews.filter(confirmed=True)
        return ProductReviewSerializer(query_set, many=True).data

    def get_subcategory_detail(self,instance):
        return SubcategorySerializer(instance.subcategory).data

class DiscountCodeSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    class Meta:
        model = DiscountCode
        fields = [
            # 'is_used',
            'code',
            'percentage',
            'maximum_value',
            'expire_at',
            # 'inventory',
            "final_price"
        ]
    def get_final_price(self, obj):
        # var_id = self.context.get("var_id")
        ## number_of_people = self.context.get("number_of_people")

        basket = self.context.get("basket")

        today = date.today()
        discount = 0
        max_discount_value = 0
        if  today < obj.expire_at: # and obj.inventory>0
            discount = obj.percentage
            max_discount_value = obj.maximum_value
        else :
            raise ParseError(detail={"error": "discount is expired", "error_code": "4006"})


        #change to for loop
        populate_items_price=0
        for item in basket:
            try:
                variation_object = ProductVariation.objects.get(id=item["var_id"])
                effective_price = variation_object.discount_price if variation_object.discount_price else variation_object.price
                populate_items_price+= (item["qty"] * float(effective_price)) #todo check for outcome
            except:
                ParseError(detail={"error": "product not found", "error_code": "4007"})


        # var = ProductVariation.objects.get(id=var_id)
        # effective_price = var.discount_price if var.discount_price else var.base_price
        # p = number_of_people *float(effective_price) #populate_items_price hamoon p hast
        #

        #TODO : HATMAN BA ELNAZ MATRAH KON
        if discount != 0:
            # max_discount_value = convert(currency, max_discount_value)
            if (float(populate_items_price) < float(max_discount_value) or  max_discount_value ==0):
                final_price =round( (float(populate_items_price) - (float(populate_items_price) * float(discount) / 100.0)))
            else:
                final_price = round(float(populate_items_price) - (float(max_discount_value) * float(discount) / 100.0))
        else :
            raise ParseError(detail={"error": "discount is zero", "error_code": "4007"})
        return decimal.Decimal("{:.2f}".format(final_price))



class PromotionalCodeSerializer(serializers.ModelSerializer):
    var_price = serializers.SerializerMethodField()
    class Meta:
        model = PromotionalCode
        fields = '__all__'

    def get_var_price(self, obj):
        request = self.context.get("request")
        basket = self.context.get("basket")

        today = date.today()
        discount = 0
        max_discount_value = 0
        if bool(request.user and request.user.is_authenticated):
            if  today < obj.expire_at: #todo inventory? (obj.inventory > 0 and) come back and discuss it after INVOICE
                discount = obj.percentage
                max_discount_value = obj.maximum_value
            else:
                raise ParseError(detail={"error": "discount is expired", "error_code": "4006"})

        populate_items_price=0
        for item in basket:
            try:
                variation_object = ProductVariation.objects.get(id=item["var_id"])
                effective_price = variation_object.discount_price if variation_object.discount_price else variation_object.price
                populate_items_price+= item["qty"] * float(effective_price) #todo check for outcome
            except:
                ParseError(detail={"error": "product not found", "error_code": "4007"})


        if discount != 0:
            if (float(populate_items_price) < float(max_discount_value)):
                tour_price =round (float(populate_items_price) - (float(populate_items_price) * float(discount) / 100.0))
            else:
                tour_price =round(float(populate_items_price) - (float(max_discount_value) * float(discount) / 100.0))
        else:
            raise ParseError(detail={"error": "discount is zero", "error_code": "4001"})
        return decimal.Decimal("{:.2f}".format(tour_price))


# todo : variation ha ham agar to invoice ii boodan shadow delete eshoon kon
class OrderedItemSerializer(serializers.ModelSerializer):
    # product_item_info = serializers.SerializerMethodField() #variation
    # I get the name of the product variation here
    # product_variation_item = serializers.StringRelatedField()
    class Meta:
        model = OrderedItem
        # IMP: I  use unit price so your previous invoices won't be incorrect after you changed a food's price.
        fields = (
            'pk',
            'product_variation_item',
            'choices',
            'qty',
            'unit_base_price',  # todo  tooye save hatman ino az variation begir
            'unit_discount_price',  # todo  tooye save hatman ino az variation begir
            # 'invoice' #????????
        )
        read_only_fields = ('pk', 'unit_base_price', 'unit_discount_price')
    # def create(self ,validated_data):
    #     v= validated_data
    #     pass
class TestInPlaceSerializer(serializers.ModelSerializer):
    orders = OrderedItemSerializer(many=True)
    # customer_info = serializers.SerializerMethodField()
    class Meta:
        model = TestInPlace
        fields = (
            'pk',
            'shipping_number',  # todo ????
            'deliver_status',
            'customer',
            'orders',
            'date',
            'address',
            'description',
            # 'transaction'
        )
        read_only_fields = ('deliver_status',"date",'customer',) #todo?

    # def get_customer_info(self,obj):
    #     customer_id=obj.customer
    #     customer_serializer = CustomerSerializer(obj.customer)
    #     res = customer_serializer.data
    #     return res

    def create(self, validated_data):
        basket = validated_data.pop('orders')
        try:
            address = validated_data.pop("address")
        except:
            pass #please add address
        shipping_price = 0
        tip = TestInPlace(**validated_data)
        tip.customer = self.context["request"].user
        tip.deliver_status = "pe"
        tip.order_status = "dr"
        tip.address = address
        tip.shipping_price = shipping_price
        tip.save()
        return tip


class InvoiceSerializer(serializers.ModelSerializer):
    orders = OrderedItemSerializer(many=True)
    # customer_info = serializers.SerializerMethodField()

    class Meta:
        model = Invoice

        fields = (
            'pk',
            'shipping_number',  # todo ????
            'order_status',
            'deliver_status',
            'customer',
            'orders',
            # todo??????benazaram bejash code ro to view begir inja bezaresh tooye gheymat?
            'discount_code',
            'total_price',
            'date',
            'address',
            'description',
            'wallet'
            # 'transaction'
        )
        read_only_fields = ('order_status','deliver_status','discount_code','total_price',"date",'customer',) #todo?

    # def get_customer_info(self,obj):
    #     customer_id=obj.customer
    #     customer_serializer = CustomerSerializer(obj.customer)
    #     res = customer_serializer.data
    #     return res

    def create(self, validated_data):
        basket = validated_data.pop('orders')
        try:
            address = validated_data.pop("address")
        except:
            pass #please add address
        order_status = "draft"

        total_price = 0
        today = date.today()
        discount = self.context["discount"]
        max_discount_value = 0
        if discount:
            if today < discount.expire_at:  # and obj.inventory>0
                discount = discount.percentage
                max_discount_value = discount.maximum_value
            else:
                raise ParseError(
                    detail={"error": "discount is expired", "error_code": "4006"})
        else:
            discount = 0
        # change to for loop
        populate_items_price = 0
        for item in basket:
            try:    
                effective_price = dict(item)['product_variation_item'].discount_price if dict(item)['product_variation_item'].price   else  dict(item)['product_variation_item'].discount_price 
                choices = dict(item)['choices']
                choices_price = decimal.Decimal("0.0")
                for choice in choices:
                    choices_price += choice.price
                effective_price += choices_price
                populate_items_price += (dict(item)["qty"] * float(effective_price))
            except Exception as e:
                print(e)
                ParseError(
                    detail={"error": "product not found", "error_code": "4007"})

        # var = ProductVariation.objects.get(id=var_id)
        # effective_price = var.discount_price if var.discount_price else var.base_price
        # p = number_of_people *float(effective_price) #populate_items_price hamoon p hast
        #
        final_price = populate_items_price
        if discount != 0:
            # max_discount_value = convert(currency, max_discount_value)
            if (float(populate_items_price) < float(max_discount_value) or max_discount_value == 0):
                final_price = round((float(
                    populate_items_price) - (float(populate_items_price) * float(discount) / 100.0)))
            else:
                final_price = round(float(
                    populate_items_price) - (float(max_discount_value) * float(discount) / 100.0))
        # else:
        #     raise ParseError(
        #         detail={"error": "discount is zero", "error_code": "4007"})
        
        # set config vat 
        vat = 0
        vtax = round(float(vat) * float(final_price) / 100.0)
        final_price = round(float(
                    populate_items_price) + (float(vat) * float(final_price) / 100.0))
        
        shipping_price = 0
        final_price = shipping_price +final_price
        final_price = decimal.Decimal("{:.2f}".format(final_price))
        invoice = Invoice(**validated_data)
        invoice.total_price = final_price
        invoice.customer = self.context["request"].user
        invoice.deliver_status = "pe"
        invoice.order_status = "dr"
        invoice.address = address
        invoice.shipping_price = shipping_price
        invoice.vtax = vtax 
        if self.context["discount_type"] == "discount":
            invoice.discount_code = discount
        elif  self.context["discount_type"] == "promotional":
            invoice.promotional_code = discount
        invoice.save()
        return invoice


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = (
            'pk',
            # 'invoice', #???
            'refId',
            'bankRefId',
            'status',
            # 'statusNum' ???
            'authority'
        )


class UserWalletSerializer(serializers.ModelSerializer):
    wallet = PresentablePrimaryKeyRelatedField(
        queryset=Wallet.objects.all(),
        presentation_serializer=WalletSerializer,
        read_source=None
    )
    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super(UserWalletSerializer, self).run_validators(value)
    def create(self, validated_data):
        instance, _ = UserWallet.objects.get_or_create(**validated_data,defaults={'value': decimal.Decimal(0.0)})
        return instance
    class Meta:
        model = UserWallet
        fields = ('user','wallet','value')
        read_only_fields = ['value']

        
class ShopRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopRequest
        fields = '__all__'

