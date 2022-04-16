from users_info.serializers import AddressSerializer, UserAddressSerializer
from django.contrib.auth.models import Group
from auth_rest_phone.serializers import AdminUserCreateSerializer, UserCreateSerializer, UserSerializer
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from shop import models, serializers
from pages import models as pages_models
from pages import serializers as pages_serializers

from shop_admin import serializers as admin_serializers
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from django.contrib.auth import get_user_model
import copy
# UserProfile = get_user_model()
User = get_user_model()
# Create your views here.

class PageContentViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = pages_models.PageContent.objects.all()
    serializer_class = pages_serializers.PageContentSerializer
    
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
            serializer = serializers.ProductDetailSerializer(page, many=True,context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ProductDetailSerializer(queryset, many=True,context={"request":request})
        return Response(serializer.data)


class ProductVariationViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ProductVariation.objects.all()
    serializer_class = admin_serializers.VariationAdminSerializer

class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Shop.objects.all()
    serializer_class = admin_serializers.ShopCreateSerializer
    def list(self,request):
        queryset = models.Shop.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.ShopSerializer(page, many=True,context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ShopSerializer(queryset, many=True,context={"request":request})
        return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.ShopSerializer(instance)
        return Response(serializer.data)

class ShopUserListView(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        group = Group.objects.get(name='shop_manager') 
        self.queryset = User.objects.filter(groups=group)
        return super().get_queryset()

class ShopUserCreateView(CreateAPIView):
    serializer_class = AdminUserCreateSerializer
    def create(self, request, *args, **kwargs):
        addresses = request.data.pop("addresses",None)
        data=request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        group = Group.objects.get(name='shop_manager') 
        group.user_set.add(user)
        if addresses is not None:
            for address in addresses:
                address["user"]=user.id
                address_serializer = AddressSerializer(data=address)
                if address_serializer.is_valid(raise_exception=True):
                    address_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        return serializer.save()

class ShopUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    # def 
    def get_queryset(self):
        group = Group.objects.get(name='shop_manager') 
        self.queryset = User.objects.filter(groups=group)    
        return super().get_queryset()

    def get_serializer_context(self):
        try:
            return   {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self,
                'user_id':self.kwargs["pk"]
            }
        except:
            return   {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self,
            }
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data =request.data

        for address in data['addresses']:
            address.update({"user":kwargs["pk"]})
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)
        
class ProductAttributeViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ProductAttribute.objects.all()
    serializer_class = serializers.ProductAttributeSerializer

class ProductAttributeChoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ChoiceAttribute.objects.all()
    serializer_class = admin_serializers.ChoiceAttributeAdminSerializer

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


class ProductBoxViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProductBox class"""

    queryset = models.ProductBox.objects.all()
    serializer_class = admin_serializers.ProductBoxSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductInstanceViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProductInstance class"""

    queryset = models.ProductInstance.objects.all()
    serializer_class = admin_serializers.ProductInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]



class NProductInstanceCreateAPIView(CreateAPIView):
    '''set count for n create'''
    queryset = models.ProductInstance.objects.all()
    serializer_class = admin_serializers.ProductInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        count = int(request.data.pop("count",1))
        for i in range(count):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({"count":count}, status=status.HTTP_201_CREATED)

class NProductBoxCreateAPIView(CreateAPIView):
    '''set count for n create'''
    queryset = models.ProductBox.objects.all()
    serializer_class = admin_serializers.ProductBoxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        count = int(request.data.pop("count",1))
        for i in range(count):
            data = copy.deepcopy(request.data)
            data["name"] = data.get("name")+" " +str(i+1)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        return Response({"count":count}, status=status.HTTP_201_CREATED)

class SendProductBoxesTo(APIView):
    '''set list of boxes in boxid_list and shop or depot as depot_id or shop_id'''
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        depot_id = int(request.data.pop("depot_id",0))
        shop_id = int(request.data.pop("shop_id",0))
        boxid_list = (request.data.pop("boxid_list",[]))
        shop = None
        depot = None
        if boxid_list :
            if depot_id:
                try :
                    depot = models.Depot.objects.get(id=depot_id)
                except models.Depot.DoesNotExist:
                    return Response({"error":"depot_does_not_exist"}, status=status.HTTP_400_BAD_REQUEST)
            elif shop_id:
                try :
                    shop = models.Shop.objects.get(id=shop_id)
                except models.Shop.DoesNotExist:
                    return Response({"error":"shop_does_not_exist"}, status=status.HTTP_400_BAD_REQUEST)

            for boxid in boxid_list:
                try:
                    box = models.ProductBox.objects.get(id=boxid)
                except models.ProductBox.DoesNotExist:
                    return Response({"error":"box_does_not_exist"}, status=status.HTTP_400_BAD_REQUEST)
                if depot_id:
                    transfer = models.ProductBoxTransfer()
                    transfer.box = box
                    transfer.from_depot =  box.depot
                    transfer.from_shop = box.shop
                    transfer.to_depot = depot
                    transfer.save()
                    box.depot = depot
                    box.shop = None
                    box.save()
                elif shop_id :
                    transfer = models.ProductBoxTransfer()
                    transfer.box = box
                    transfer.from_depot =  box.depot
                    transfer.from_shop = box.shop
                    transfer.to_shop = shop
                    transfer.save()
                    box.shop = shop
                    box.depot = None
                    box.save()
        return Response({"boxid_list":boxid_list}, status=status.HTTP_201_CREATED)

    

class AssignProductToBoxAPIView(APIView):
    '''set list of instances in instanceid_list and boxid as box_id'''
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        instanceid_list = (request.data.pop("instanceid_list",[]))
        box_id = int(request.data.pop("box_id",0))
        if instanceid_list and box_id :
            instance_count = len(instanceid_list)
            try:
                box = models.ProductBox.objects.get(id=box_id)
            except models.ProductBox.DoesNotExist:
                return Response({"error":"box_does_not_exist"}, status=status.HTTP_400_BAD_REQUEST)

            count_inbox = box.count_in_box
            instance_inbox =len (box.productinstances.all())
            if instance_count > count_inbox - instance_inbox :
                return Response({"error":"box_out_of_"}, status=status.HTTP_400_BAD_REQUEST)
            for instanceid in instanceid_list:
                try:
                    instance = models.ProductInstance.objects.get(id=instanceid)
                    if instance.box :
                        return Response({"error":"instance_had_box","instanceid":instanceid}, status=status.HTTP_400_BAD_REQUEST)
                except models.ProductInstance.DoesNotExist:
                        return Response({"error":"instance_does_not_exist","instanceid":instanceid}, status=status.HTTP_400_BAD_REQUEST)
            for instanceid in instanceid_list:
                instance = models.ProductInstance.objects.get(id=instanceid)
                instance.box = box
                instance.save()
        return Response({"instanceid_list":instanceid_list,"box_id":box_id}, status=status.HTTP_201_CREATED)
    def patch(self, request, *args, **kwargs):
        instanceid_list = (request.data.pop("instanceid_list",[]))
        if instanceid_list :
            for instanceid in instanceid_list:
                try:
                    instance = models.ProductInstance.objects.get(id=instanceid)
                    instance.box = None
                    instance.save()
                except models.ProductInstance.DoesNotExist:
                    return Response({"error":"instance_does_not_exist","instanceid":instanceid}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"instanceid_list":instanceid_list}, status=status.HTTP_201_CREATED)


class DepotViewSet(viewsets.ModelViewSet):
    """ViewSet for the Depot class"""

    queryset = models.Depot.objects.all()
    serializer_class = admin_serializers.DepotSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductBoxTransferListAPIView(ListAPIView):
    queryset = models.ProductBoxTransfer.objects.all()
    serializer_class = admin_serializers.ProductBoxSerializer
    permission_classes = [permissions.IsAuthenticated]


#TODO check box for latest update
class ProductBoxTransferRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.ProductBoxTransfer.objects.all()
    serializer_class = admin_serializers.ProductBoxSerializer
    permission_classes = [permissions.IsAuthenticated]
    def update(self, request, *args, **kwargs):
        boxid = request.data.get("box")
        try:
            box = models.ProductBox.objects.get(id=boxid)
        except models.ProductBox.DoesNotExist:
            return Response({"error":"box_does_not_exist"}, status=status.HTTP_400_BAD_REQUEST)
        box.shop = request.data.get("to_shop")
        box.depot = request.data.get("to_depot")
        return super().update(request, *args, **kwargs)

class VariationGlassChoiceRetrieveAPIView(RetrieveAPIView):
    queryset = models.ProductVariation.objects.all()
    serializer_class = admin_serializers.VariationGlassChoiceAdminSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShopRequestViewSet(viewsets.ModelViewSet):
    queryset = models.ShopRequest.objects.all()
    serializer_class = serializers.ShopRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


class PromotionalCodeViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.PromotionalCode.objects.all()
    serializer_class = admin_serializers.PromotionalCodeSerializer

class DiscountCodeViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.DiscountCode.objects.all()
    serializer_class = admin_serializers.DiscountCodeSerializer

class OccasionalDiscountViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.OccasionalDiscount.objects.all()
    serializer_class = admin_serializers.OccasionalDiscountSerializer
