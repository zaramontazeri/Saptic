from re import A
import sys

from decimal import Decimal
from django.core import validators
from django.shortcuts import render
# from requests import Response
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework import viewsets, permissions, status
# Create your views here.
from rest_framework.views import APIView

from shop.models import ChargeTransaction, Shop, Product, OrderedItem, Invoice, DiscountCode, ProductVariation, \
    PromotionalCode, Subcategory,Transactions,Category, UserWallet, Wallet
from shop.filterset import ProductListFilter, MyFilterBackend
from shop.serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, \
    RelatedProductSerializer, DiscountCodeSerializer, PromotionalCodeSerializer,InvoiceSerializer,SubcategorySerializer, UserWalletSerializer
from services.payment import *
from django.views import View

class CategoryListAPIView(ListAPIView): #just category (without sub category
    queryset = Category.objects.all()
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
        query_params = self.request.query_params
        query_key_exclude = ['max_price', 'min_price', 'category', 'subcategory', 'test_in_place', 'attribute', 'attribute_value', 'ordering', 'color']

        query_keys = list(query_params.keys() - query_key_exclude)
        print (query_params)
        queryset=Product.objects.all()
        for i in query_keys:
            query_list = query_params[i].split("~")
            print(i,query_list)
            queryset = queryset.filter(variations__specifications__attribute__slug = i , \
                variations__specifications__slug__in=query_list)
        return queryset
    def get_serializer_context(self):
        context =  super().get_serializer_context()
        color = self.request.query_params.get("color",None)
        if color:
            context["colors"] = color.split("~")
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubcategoryListAPIView(ListAPIView): #show all of subcategories of a category
    serializer_class = SubcategorySerializer
    def get_queryset(self):
        c_id = self.kwargs['c_id']
        if c_id > 0:
            queryset=Subcategory.objects.filter(category__id=c_id)
        else :
             queryset=Subcategory.objects.all()
        return queryset


# class MenuItemProductsListAPIView(ListAPIView): #after clicking on each sub category filter
#     pass


class ProductDetailView(RetrieveAPIView): #send with all Variations
    queryset = Product.objects.all() #filter(product_reviews__confirmed=True)
    serializer_class =ProductDetailSerializer
    lookup_field="slug"

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


class UserWalletDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,wallet_id):
        data={}
        data["user"] = request.user
        data['wallet'] = wallet_id
        serializer = UserWalletSerializer(data=data)
        if serializer.is_valid():
            serializer.save()    
        return Response(serializer.data)

class UserWalletsInfoList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qs = UserWallet.objects.filter(user =self.request.user)
        return qs  
    def get_serializer_class(self):
        wallets = Wallet.objects.all()
        
        for wallet in wallets :
            data = {"user":self.request.user.id,"wallet":wallet.id}
            serializer = UserWalletSerializer(data=data)
            if serializer.is_valid():
                serializer.save()   
        self.serializer_class = UserWalletSerializer
        return super().get_serializer_class()     

class WalletCharge(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,wallet_id):
        request_data ={}
        request_data["amount"] = request.data['value']
        # request_data["description"] = invoice_ser.data.get('description'," ?????? ")
        request_data["description"] = "??????"
        value = request.data.get('value')
        data= {}
        data["user"] = request.user
        data['wallet'] = wallet_id
        serializer = UserWalletSerializer(data=data)
        instance = None
        if serializer.is_valid():
            instance = serializer.save()   
        status,url, authority= send_request(request ,request_data)
        if status == "success":
            ChargeTransaction.objects.create(wallet_charge=instance,
                                        status="pending",statusNum=0,authority=authority,value=value)
            return Response({"url":url,"status":status})
        elif status == "failed":
            return Response({"status":status})


class VerifyCharge(View):
    def get(self, request):
        authority = request.GET['Authority']
        transaction = ChargeTransaction.objects.get(authority=authority)
        value = transaction.value
        status , refes = verify(request,float(value))
        if status == "success":
            transaction.status="payed"
            transaction.refId = refes
            transaction.save()
            wch = transaction.wallet_charge
            wch.value = wch.value+value
            wch.save()
            return render(request, status + '.html',
                          {

                          })
            
        elif status == "failed":
            transaction.status="failed"
            transaction.statusNum = refes
            transaction.save()
            return render(request, status + '.html',
                          {

                          })
        elif status == "cancel":
            transaction.status = "cancel"
            transaction.statusNum = refes
            transaction.save()
            return render(request, status + '.html',
                          {

                          })
class InvoiceView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class=InvoiceSerializer
    def get_queryset(self):
        return Invoice.objects.filter(customer =self.request.user)
    def create(self, request, *args, **kwargs):
        # basket = request.DATA["POST"].get('basket') It's how django itself works
        code = request.data.get("code", None) #IMP: yek nafar nmitoone ham discount code estefade kone ham promotional code
        user = request.user
        context = {
            "request": request,
            "discount" : None,
            "discount_type":None,
        }
        try:
            discount = DiscountCode.objects.get(code=code)
            context["discount"] = discount
            context["discount_type"] = "discount"
        except DiscountCode.DoesNotExist:
                try:
                    discount = PromotionalCode.objects.get(code=code,user=request.user)
                    context["discount"] = discount
                    context["discount_type"] = "promotional"
                except PromotionalCode.DoesNotExist:
                    # return  Response({"error_code":"4041","error":"discount  not found"}, status=status.HTTP_404_NOT_FOUND)
                    pass
        invoice_ser = InvoiceSerializer(data=request.data ,context=context)
        if invoice_ser.is_valid():
            invoice = invoice_ser.save()
        else :
            return Response(invoice_ser.errors)
        request_data ={}
        request_data["amount"] = invoice_ser.data['total_price']
        # request_data["description"] = invoice_ser.data.get('description'," ?????? ")
        request_data["description"] = "??????"
        status,url, authority= send_request(request ,request_data)
        if status == "success":
            Transactions.objects.create(invoice=invoice,
                                        status="pending",statusNum=0,authority=authority)
            return Response({"url":url,"status":status})
        elif status == "failed":
            return Response({"status":status})


class TestInPlaceView(ListCreateAPIView):
    serializer_class=InvoiceSerializer
    def get_queryset(self):
        return Invoice.objects.filter(customer =self.request.user)
    def create(self, request, *args, **kwargs):
        # basket = request.DATA["POST"].get('basket') It's how django itself works
        code = request.data.get("code", None) #IMP: yek nafar nmitoone ham discount code estefade kone ham promotional code
        context = {
            "request": request,
            "discount" : None,
            "discount_type":None,
        }
        try:
            discount = DiscountCode.objects.get(code=code)
            context["discount"] = discount
            context["discount_type"] = "discount"
        except DiscountCode.DoesNotExist:
                try:
                    discount = PromotionalCode.objects.get(code=code,user=request.user)
                    context["discount"] = discount
                    context["discount_type"] = "promotional"
                except PromotionalCode.DoesNotExist:
                    # return  Response({"error_code":"4041","error":"discount  not found"}, status=status.HTTP_404_NOT_FOUND)
                    pass
        invoice_ser = InvoiceSerializer(data=request.data ,context=context)
        invoice_ser.is_valid()
        invoice = invoice_ser.save()
        request_data ={}
        request_data["amount"] = invoice_ser.data['total_price']
        # request_data["description"] = invoice_ser.data.get('description'," ?????? ")
        request_data["description"] = "??????"
        status,url, authority= send_request(request ,request_data)
        if status == "success":
            Transactions.objects.create(invoice=invoice,
                                        status="pending",statusNum=0,authority=authority)
            return Response({"url":url,"status":status})
        elif status == "failed":
            return Response({"status":status})





#
# class OrderCreateAPIView(CreateAPIView):
#     queryset = OrderedItem.objects.all()
#     serializer_class = OrderedItemSerializer
#     def perform_create(self, serializer):
#         serializer.save(costumer=self.request.user)

