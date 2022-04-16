# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
# from django.db import connections
# from PIL import Image
# import os
# import hashlib

# from rest_framework.exceptions import PermissionDenied


# # def get_client_ip(request):
# #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
# #     if x_forwarded_for:
# #         ip = x_forwarded_for.split(',')[0]
# #     else:
# #         ip = request.META.get('REMOTE_ADDR')
# #     return ip
# from users.models import Customer


# class EmailMobileBackend:
#     def authenticate(self,request=None, email=None, password=None):
#         print("hello im",email,password)
#         user_model = get_user_model()
#         try:
#             user = user_model.objects.filter(email=email).first()

#             if user :
#                 print(user, password)
#                 if user.check_password(password):  # check valid password
#                     return user  # return user to be authenticated
#         except user_model.DoesNotExist:  # no matching user exists

#             # try:
#             #     customer = Customer.objects.get(phone_number=username)
#             #     user = customer.user
#             #     if user.check_password(password):
#             #         return user
#             # except Customer.DoesNotExist:
#             #     return None
#             return None

#     def get_user(self, user_id):
#         user_model = get_user_model()
#         try:
#             return user_model.objects.get(pk=user_id)
#         except user_model.DoesNotExist:
#             return None


# # from django.conf import settings
# # from django.contrib.auth import authenticate
# # from django.contrib.auth.backends import ModelBackend
# # from django.contrib.auth.models import User
# # from rest_framework import serializers, exceptions
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from rest_framework_simplejwt.views import TokenViewBase
# # from django.utils.translation import ugettext_lazy as _
# #
# # from burger.models  import *
# # from django.core.files import File
# # class MobileBackend:
# #     def authenticate(self, request, phone_number=None, rand_number=None):
# #         customer = Customer.objects.get(phone_number=phone_number)
# #         m_request = MobileRequest.objects.filter(phone_number=phone_number).order_by('-id')[0]
# #         if customer :
# #             if m_request and m_request.rand_number == rand_number:
# #                 user = customer.user
# #                 return user
# #         return None
# #
# #     def get_user(self, user_id):
# #         try:
# #             return User.objects.get(pk=user_id)
# #         except User.DoesNotExist:
# #             return None
# #
# # class MobilePasswordBackend:
# #     def authenticate(self, request, phone_number=None, password=None):
# #         customer = Customer.objects.get(phone_number=phone_number)
# #         if customer.user.check_password(password):
# #             return customer.user
# #         return None
# #
# #     def get_user(self, user_id):
# #         try:
# #             return User.objects.get(pk=user_id)
# #         except User.DoesNotExist:
# #             return None
# #
# # class MobileTokenObtainSerializer(serializers.Serializer):
# #     default_error_messages = {
# #         'no_active_account': _('No active account found with the given credentials')
# #     }
# #
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #
# #         self.fields['phone_number'] = serializers.CharField()
# #         self.fields['rand_number'] = serializers.IntegerField()
# #
# #     def validate(self, attrs):
# #         authenticate_kwargs = {
# #             "phone_number": attrs["phone_number"],
# #             'rand_number': attrs['rand_number'],
# #         }
# #         try:
# #             authenticate_kwargs['request'] = self.context['request']
# #         except KeyError:
# #             pass
# #
# #         self.user = authenticate(**authenticate_kwargs)
# #
# #         # Prior to Django 1.10, inactive users could be authenticated with the
# #         # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
# #         # prevents inactive users from authenticating.  App designers can still
# #         # allow inactive users to authenticate by opting for the new
# #         # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
# #         # users from authenticating to enforce a reasonable policy and provide
# #         # sensible backwards compatibility with older Django versions.
# #         if self.user is None or not self.user.is_active:
# #             raise exceptions.AuthenticationFailed(
# #                 self.error_messages['no_active_account'],
# #                 'no_active_account',
# #             )
# #
# #         return {}
# #
# #     @classmethod
# #     def get_token(cls, user):
# #         raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')
# #
# #
# # class MobileTokenObtainPairSerializer(MobileTokenObtainSerializer):
# #     @classmethod
# #     def get_token(cls, user):
# #         return RefreshToken.for_user(user)
# #
# #     def validate(self, attrs):
# #         data = super().validate(attrs)
# #
# #         refresh = self.get_token(self.user)
# #
# #         data['refresh'] = str(refresh)
# #         data['access'] = str(refresh.access_token)
# #
# #         return data
# #
# # class MobileTokenObtainPairView(TokenViewBase):
# #     """
# #     Takes a set of user credentials and returns an access and refresh JSON web
# #     token pair to prove the authentication of those credentials.
# #     """
# #     serializer_class = MobileTokenObtainPairSerializer
# #
# #
# #
# #
# # class SellerBackend(ModelBackend):
# #     def authenticate(self, request, username=None, password=None):
# #         # seller = Customer.objects.get(phone_number=phone_number)
# #         # m_request = MobileRequest.objects.filter(phone_number=phone_number).order_by('-id')[0]
# #         # if customer :
# #         #     if m_request and m_request.rand_number == rand_number:
# #         #         user = customer.user
# #         #         return user
# #         # return None
# #         user = super().authenticate(username,password)
# #         if user :
# #             seller = Seller.objects.get(user=user)
# #             if seller :
# #                 return user
# #             else :
# #                 return None
# #         else :
# #             return None
# #
# # class SellerTokenObtainSerializer(serializers.Serializer):
# #     default_error_messages = {
# #         'no_active_account': _('No active account found with the given credentials')
# #     }
# #
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #
# #         self.fields['username'] = serializers.CharField()
# #         self.fields['password'] = serializers.CharField()
# #
# #     def validate(self, attrs):
# #         authenticate_kwargs = {
# #             "username": attrs["username"],
# #             'password': attrs['password'],
# #         }
# #         try:
# #             authenticate_kwargs['request'] = self.context['request']
# #         except KeyError:
# #             pass
# #
# #         self.user = authenticate(**authenticate_kwargs)
# #
# #         # Prior to Django 1.10, inactive users could be authenticated with the
# #         # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
# #         # prevents inactive users from authenticating.  App designers can still
# #         # allow inactive users to authenticate by opting for the new
# #         # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
# #         # users from authenticating to enforce a reasonable policy and provide
# #         # sensible backwards compatibility with older Django versions.
# #         if self.user is None or not self.user.is_active:
# #             raise exceptions.AuthenticationFailed(
# #                 self.error_messages['no_active_account'],
# #                 'no_active_account',
# #             )
# #
# #         return {}
# #
# #     @classmethod
# #     def get_token(cls, user):
# #         raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')
# #
# #
# # class SellerTokenObtainPairSerializer(SellerTokenObtainSerializer):
# #     @classmethod
# #     def get_token(cls, user):
# #         return RefreshToken.for_user(user)
# #
# #     def validate(self, attrs):
# #         data = super().validate(attrs)
# #
# #         refresh = self.get_token(self.user)
# #
# #         data['refresh'] = str(refresh)
# #         data['access'] = str(refresh.access_token)
# #
# #         return data
# #
# # class SellerTokenObtainPairView(TokenViewBase):
# #     """
# #     Takes a set of user credentials and returns an access and refresh JSON web
# #     token pair to prove the authentication of those credentials.
# #     """
# #     serializer_class = SellerTokenObtainPairSerializer
