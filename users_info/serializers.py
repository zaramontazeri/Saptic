# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
# from django.db import IntegrityError, transaction

# from django.core import exceptions as django_exceptions

# from auth_rest.conf import settings
# # from tours.serializers import TourPaymentSerializer
# from users.models import Customer
from auth_rest_phone.conf import settings
from django.db.models import manager
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Address
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission
# from django.db.models import Exists, OuterRef, Q
# from django.utils.deprecation import RemovedInDjango31Warning
from auth_rest_phone.compat import get_user_email, get_user_email_field_name

User = get_user_model()
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'password')

#     def save(self, request):
#         user = User.objects.create_user(
#             first_name=request.data.get('first_name'),
#             last_name=request.data.get('last_name'),
#             username=request.data.get('username'),
#             password=request.data.get('password'),
#         )
#         return user


# class UserSerializer(serializers.ModelSerializer):
#     phone =serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username','email','phone']

#     def get_phone(self,obj):

#         customer = Customer.objects.filter(user=self.context['request'].user).first()
#         if customer:
#             return customer.phone
#         else :
#             return -1

# class ProfileSerializer(serializers.ModelSerializer):
#     phone = serializers.SerializerMethodField()
#     payments = serializers.SerializerMethodField()
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'phone','payments']

#     def get_phone(self,obj):
#         customer = Customer.objects.filter(user=obj).first()
#         # customer = Customer.objects.filter(user=self.context['request'].user).first()

#         if customer:
#             return customer.phone
#         else :
#             return -1
#     def get_payments(self,obj):
#         payments = obj.payments.all()
#         if payments:
#             return TourPaymentSerializer(payments, many=True).data
#         else:
#             return -1


# class UserPhoneNumberCreateSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(style={"input_type": "password"}, write_only=True)
#     phone_number = serializers.CharField( write_only=True)
#     default_error_messages = {
#         "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
#     }

#     class Meta:
#         model = User
#         fields = tuple(User.REQUIRED_FIELDS) + (
#             settings.LOGIN_FIELD,
#             settings.USER_ID_FIELD,
#             "password",
#             "phone_number"
#         )

#     def validate(self, attrs):
#         phone_number = attrs.pop("phone_number")
#         user = User(**attrs)
#         password = attrs.get("password")
#         email = attrs.get("email")
#         username = attrs.get("username")
#         attrs["phone_number"]=phone_number

#         try:
#             validate_password(password, user)
#         except django_exceptions.ValidationError as e:
#             serializer_error = serializers.as_serializer_error(e)
#             raise serializers.ValidationError(
#                 {"password": serializer_error["non_field_errors"]}
#             )
#         if User.objects.filter(email=email).exclude(username=username).exists():
#             raise serializers.ValidationError({"email":"email_exist","error_code":"40010"})
#         return attrs

#     def create(self, validated_data):
#         try:
#             user = self.perform_create(validated_data)
#         except IntegrityError:
#             self.fail("cannot_create_user")

#         return user

#     def perform_create(self, validated_data):
#         with transaction.atomic():
#             print(validated_data)
#             phone_number = validated_data.pop("phone_number")
#             user = User.objects.create_user(**validated_data)
#             customer = Customer()
#             customer.phone = phone_number
#             customer.user = user
#             customer.save()
#             if settings.SEND_ACTIVATION_EMAIL:
#                 user.is_active = False
#                 user.save(update_fields=["is_active"])

#         return user


# class UserPhoneNumberCreatePasswordRetypeSerializer(UserPhoneNumberCreateSerializer):
#     default_error_messages = {
#         "password_mismatch": settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR
#     }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["re_password"] = serializers.CharField(
#             style={"input_type": "password"}
#         )

#     def validate(self, attrs):
#         self.fields.pop("re_password", None)
#         re_password = attrs.pop("re_password")
#         attrs = super().validate(attrs)
#         if attrs["password"] == re_password:
#             return attrs
#         else:
#             self.fail("password_mismatch")


# class CustomerSerializer(serializers.ModelSerializer):
#   user =  UserSerializer
#   class Meta:
#     model = Customer
#     fields = '__all__'



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields = "__all__"

class UserAddressSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False)
    addresses = AddressSerializer(many=True) 
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD, "email", "first_name", "last_name", "avatar",'addresses'
        )
        read_only_fields = (settings.LOGIN_FIELD,)

    def update(self, instance, validated_data):
        addresses = validated_data.pop('addresses')
        remove_items = { item.id: item for item in instance.addresses.all() }
        context = {}
        context["user"]= instance
        context["request"]= self.context.get("request",None)
        for item in addresses:
            item_id = item.get("id", None)
            if item_id is None:
                # new item so create this
                item['user']=instance.id
                serializer = AddressSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()    
            elif remove_items.get(item_id, None) is not None:
                # update this item
                instance_item = remove_items.pop(item_id)
                item['user']=instance.id
                serializer = Address(instance_item, data=item)
                if serializer.is_valid():
                    serializer.save()
        for item in remove_items.values():
            item.delete()
        for field in validated_data:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))
        return instance
        # return super().update(instance, validated_data)
