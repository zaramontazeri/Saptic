import sys

from decimal import Decimal
from django.shortcuts import render
# from requests import Response
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework import viewsets, permissions, status
# Create your views here.
from rest_framework.views import APIView

from shop.models import Shop, Product, Menuitem, OrderedItem, Invoice, DiscountCode, ProductVariation, \
    PromotionalCode
from shop.filterset import ProductListFilter, MyFilterBackend
from shop.serializers import CategorySerializer, ProductListSerializer, MenuitemSerializer, ProductDetailSerializer, \
    RelatedProductSerializer, DiscountCodeSerializer, PromotionalCodeSerializer,InvoiceSerializer


class CategoryListAPIView(ListAPIView): #just category (without sub category
    queryset = Shop.objects.all()
    serializer_class = CategorySerializer


class ProductsCategoryListAPIView(ListAPIView):
    serializer_class =   ProductListSerializer
    filter_backends = [MyFilterBackend] #todo BIG TODO FiLTER WITH ERFAN
    filter_class = ProductListFilter
    def get_queryset(self):
        c_id = self.kwargs['c_id']
        if c_id > 0:
            queryset=Product.objects.filter(menuitem__category__id=self.kwargs['c_id'])
        else :
            queryset=Product.objects.all()
        return queryset

class ProductsListAPIView(ListAPIView):
    serializer_class =   RelatedProductSerializer
    filter_backends = [MyFilterBackend] #todo BIG TODO FiLTER WITH ERFAN
    filter_class = ProductListFilter
    def get_queryset(self):
        queryset=Product.objects.all()
        return queryset

class MenuItemListAPIView(ListAPIView): #show all of subcategories of a category
    serializer_class = MenuitemSerializer
    def get_queryset(self):
        c_id = self.kwargs['c_id']
        if c_id > 0:
            queryset=Menuitem.objects.filter(category__id=c_id)
        else :
             queryset=Menuitem.objects.all()
        return queryset


# class MenuItemProductsListAPIView(ListAPIView): #after clicking on each sub category filter
#     pass


class ProductDetailView(RetrieveAPIView): #send with all Variations
    #todo product -hatman related products ham ezafe kon -
    #todo  variation with all information and specifications -
    queryset = Product.objects.all() #filter(product_reviews__confirmed=True)
    serializer_class =ProductDetailSerializer


# class OrderedItemViewSet(viewsets.ModelViewSet):
#     """ViewSet for the OrderItem class"""
#     queryset = OrderedItem.objects.all()
#     serializer_class = OrderedItemSerializer
#
#

    # permission_classes = [permissions.IsAuthenticated] todo what about permition?
    # def destroy(self, request, *args, **kwargs):
    #    user = request.user # deleting user
    #    # you custom logic #
    #    instance = self.get_object()
    #    invoice = instance.invoice
    #    if invoice:
    #        qty = instance.qty
    #        up = instance.orderd_item_unit_price
    #        price = qty*up
    #        invoice.price
    #
    #    return super(OrderedItemViewSet, self).destroy(request, *args, **kwargs)


# class DiscountCheck(APIView):
#
#     # permission_classes = [permissions.IsAuthenticated] #todo  neshoon bede ke user request.user hast shayad ye permision benevis: isOwner . baraye address ham hamin karo kon
#     def post(self,request):
#         # {"code": 2,
#         #  "basket":[  {"var_id":1, "qty":2} , {"var_id":2, "qty":1} ]
#         #  }
#
#         code = request.data.get("code",None) #rest framework way
#         #code = request.DATA["POST"].get('code') #django way
#         basket = request.data.get("basket",None)  # it has all var_id and their qty
#
#
#         # var_id = request.data.get("var_id",None)
#         # currency =  request.data.get("currency","AED")
#         # number_of_people = request.data.get("number_of_people")
#         context = {
#             # "var_id": var_id,
#             # "number_of_people":number_of_people,
#             "request": request #why?
#             # "currency":currency
#         }
#
#
#         try:
#             if code: #if not None:
#                 discount_object = DiscountCode.objects.get(code=code)
#                 sum=0
#
#
#                 # var_id_list=[]
#                 # for item in basket: #Make a list that shows all of variation id's
#                 #     var_id_list.append(item["var_id"])
#                 # #### variation_objects=ProductVariation.objects.filter(pk__in=var_id_list)
#
#                 try:
#                     for item in basket:
#                         # sum = qty*price
#                         variation_object=ProductVariation.objects.get(id=item["var_id"])
#                         if variation_object.discount_price:
#                             sum += variation_object.discount_price*item["qty"]
#                         else:
#                             sum +=variation_object.price*item["qty"]
#
#                     dis=Decimal(discount_object.percentage/100)
#                     final_price = round(sum - sum*dis,2) #if I don't use 2 , it will be integer. but i want decimal
#
#                 except ProductVariation.DoesNotExist:
#                     return Response({"error_code": "4041", "error": "product  not found"},
#                                 status=status.HTTP_404_NOT_FOUND)
#                 # except Exception as e:
#                     # # Just print(e) is cleaner and more likely what you want,
#                     # # but if you insist on printing message specifically whenever possible...
#                     # if hasattr(e, 'message'):
#                     #     print(e.message)
#                     # else:
#                     #     print(e)
#
#                 serializer = DiscountCodeSerializer(discount_object,context=context)
#                 return Response(serializer.data,status=status.HTTP_200_OK)
#         except DiscountCode.DoesNotExist:
#             # if bool(request.user and request.user.is_authenticated):# in baraye partak elzami nist bejaye kole if else permition isAthenticated bezar  pas faghat try except ro bezar
#             return Response({"error_code": "4041", "error": "discount  not found"}, status=status.HTTP_404_NOT_FOUND)
#             #todo delete above line if you want below line
#
#              #todo ###### after talking about promotional with erfan
#             # try:
#             #     discount = PromotionalCode.objects.get(code=code,user=request.user,context=context)
#             #     serializer = PromotionalCodeSerializer(discount)
#             #     return Response(serializer.data, status=status.HTTP_200_OK)
#             # except PromotionalCode.DoesNotExist:
#             #     return  Response({"error_code":"4041","error":"discount  not found"}, status=status.HTTP_404_NOT_FOUND)
#             #
#



class DiscountCheck(APIView):
    # permission_classes = [permissions.IsAuthenticated] #todo  neshoon bede ke user request.user hast shayad ye permision benevis: isOwner . baraye address ham hamin karo kon
    def post(self,request):
        {"code": 1,
         "basket":[  {"var_id":1, "qty":2} , {"var_id":2, "qty":1} ]
         }

        code = request.data.get("code")
        basket = request.data.get("basket", None)
        context = {
            "basket":basket,
            "request": request,
        }

        try:
            discount = DiscountCode.objects.get(code=code)
            serializer = DiscountCodeSerializer(discount,context=context)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except DiscountCode.DoesNotExist:
                try:
                    discount = PromotionalCode.objects.get(code=code,user=request.user)
                    serializer = PromotionalCodeSerializer(discount,context=context)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except PromotionalCode.DoesNotExist:
                    return  Response({"error_code":"4041","error":"discount  not found"}, status=status.HTTP_404_NOT_FOUND)



class InvoiceView(ListCreateAPIView):
    model = Invoice
    #serializer

    def create(self, request, *args, **kwargs):
        # basket = request.DATA["POST"].get('basket') It's how django itself works
        code = request.data.get("code")
        basket = request.data.get("basket", None)
        address = request.data.get("address",None)
        context = {
            "basket":basket,
            "request": request,
            'address':address,
        }
        try:
            discount = DiscountCode.objects.get(code=code)
            context["discount"] = discount
        except DiscountCode.DoesNotExist:
                try:
                    discount = PromotionalCode.objects.get(code=code,user=request.user)
                    context["discount"] = discount
                except PromotionalCode.DoesNotExist:
                    return  Response({"error_code":"4041","error":"discount  not found"}, status=status.HTTP_404_NOT_FOUND)
        
        invoice = InvoiceSerializer(context=context)


#
# class OrderCreateAPIView(CreateAPIView):
#     queryset = OrderedItem.objects.all()
#     serializer_class = OrderedItemSerializer
#     def perform_create(self, serializer):
#         serializer.save(costumer=self.request.user)

