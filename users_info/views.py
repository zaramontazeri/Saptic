# # from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# # from rest_auth.registration.views import SocialLoginView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.views import APIView
# #
# from users.serializers import UserSerializer, ProfileSerializer


# # from users.models import User

# #
# # class GoogleLogin(SocialLoginView):
# #     adapter_class = GoogleOAuth2Adapter
# #
# #
# class GetMe(generics.RetrieveAPIView):
#     """
#     Retrieve User info from token
#     """
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(UserSerializer(request.user,context={"request":request}).data)

# class GetProfile(generics.RetrieveAPIView):
#     """
#     Retrieve User info from token
#     """
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(ProfileSerializer(request.user,context={"request":request}).data)


# class GetGoogle(APIView):

#     def get(self, request):
#         print (request.GET)
#         return Response({"test":"ok"})

from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from .serializers import AddressSerializer
from .models import  Address

class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = Address.objects.filter(is_active=True)
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated] #todo isOwner ham benevis khodet
    def  get_queryset(self):
        return Address.objects.filter(is_active=True,user=self.request.user)
    

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user']=request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        #instance.delete() #CHANGE
        address = self.get_object() #farghesh ba estefade az instance chie?
        address.is_active = False
        address.save()

    def update(self, request, pk=None):
        raise MethodNotAllowed('PUT', detail='Method "PUT" not allowed')

    def partial_update(self, request, pk=None):
        raise MethodNotAllowed('PATCH', detail='Method "PATCH" not allowed')