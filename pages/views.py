from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.views.generic.base import View

from pages.models import FAQ, Page, ContactMessage, Subscription, CompanyInfo
from pages.serializers import FaqSerializer, PageSerializer, ContactMessageSerializer, SubscriptionSerializer, \
    CompanyInfoSerializer,PageContentSerializer
from rest_framework.exceptions import NotFound

class FaqList(generics.ListAPIView):
    """
    List all FAQs
    """
    serializer_class = FaqSerializer
    queryset = FAQ.objects.filter(active=True)
    authentication_classes = []

    def list(self, request, format=None):
        language = request.query_params.get('LANGUAGE_CODE', 'en') #todo is it the default?
        faqs = self.queryset.filter(language=language).order_by('-priority')
        serializer = self.serializer_class(faqs, many=True)
        return Response(serializer.data)


class PageDetail(generics.RetrieveAPIView):
    """
    Page detail
    """
    serializer_class = PageSerializer
    queryset = Page.objects.filter()
    authentication_classes = []

    def get(self, request, slug, format=None):
        language = request.query_params.get('LANGUAGE_CODE', 'en')
        page = get_object_or_404(Page, language=language, active=True, slug=slug)
        serializer = self.serializer_class(page)
        return Response(serializer.data)


class ContactMessageCreate(generics.CreateAPIView):
    """
    Creating new Contact Message
    """
    serializer_class = ContactMessageSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubscriptionCreate(generics.CreateAPIView):
    """
    Creating new Subscription email
    """
    serializer_class = SubscriptionSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetail(generics.RetrieveAPIView):
    """
    Company Detail
    """
    serializer_class = CompanyInfoSerializer
    # queryset = CompanyInfo.objects.first()
    queryset = CompanyInfo.objects.all()
    authentication_classes = []

    def get(self, request, format=None):
        company = self.get_queryset().first()
        serializer = self.serializer_class(company)
        return Response(serializer.data)


# class Test(View):
#     def get(self, request, *args, **kwargs):
#
#         news_letter = NewsLetter.objects.all()[1]
#         news_serializer = NewsLetterSerializer(news_letter)
#         print (news_serializer.data)
#         context = {'news_letter': news_serializer.data}
#         return render(request, "email/news_letter_blog_type1.html", context=context)

class PageContentView(generics.RetrieveAPIView):
    """ViewSet for the PageContent class"""
    def get_queryset(self):
        try:
            print(self.kwargs["page_name"])
            query = models.PageContent.objects.filter(page_name=self.kwargs["page_name"],section= self.kwargs["section"])
        except:
            raise NotFound(detail="content not found", code=4041)

    # queryset = models.PageContent.objects.all()
    serializer_class = PageContentSerializer
    # permission_classes = [permissions.IsAuthenticated]
