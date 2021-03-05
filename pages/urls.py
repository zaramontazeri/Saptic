from django.urls import path

from pages import views
from django.views.generic import TemplateView



urlpatterns = [
    path('faq/', views.FaqList.as_view()),
    path('detail/<slug:slug>/', views.PageDetail.as_view()),
    path('contact/', views.ContactMessageCreate.as_view()),
    path('subscription/', views.SubscriptionCreate.as_view()),
    path('company/', views.CompanyDetail.as_view()),
    path('content/<str:page_name>/<str:section>', views.PageContentView.as_view()),
    # path("test",views.Test.as_view()),

]
