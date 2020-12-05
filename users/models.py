# from django.contrib.auth.models import User
# # from django.contrib.gis.db import models
# from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
# def has_tour(self, tour):
#     if self.payments.filter(tour=tour).first():
#         return True
#     return False

# User.add_to_class("has_tour", has_tour)

# UserModel = get_user_model()

# class Customer (models.Model):
#     full_name = models.CharField(max_length=250)
#     phone = models.CharField(max_length=250)
#     address = models.TextField(null=True,blank=True)
#     user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name="customer")

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=11)
    address_text = models.TextField()
    recipient_fullname = models.CharField(max_length=150)
    recipient_phone_number = models.CharField(max_length=14)  # IF FOR EXAMPLE THEY USED 0098
    is_active =models.BooleanField(default=True) #instead of delete I would change this to False