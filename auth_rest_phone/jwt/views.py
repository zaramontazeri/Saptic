from django.contrib import auth
from rest_framework_simplejwt.views import TokenViewBase

from auth_rest_phone.jwt.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenViewBase):
    authentication_classes = []
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomTokenObtainPairSerializer
