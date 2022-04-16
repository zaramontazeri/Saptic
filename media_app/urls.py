from django.urls import path
from .views import *

urlpatterns = [
    path('', FileUploadView.as_view()),
    path('list/', FileListAPIView.as_view()),
    path ('update/<int:pk>/',FileUpdateAPIView.as_view()),
    path ('delete/<int:pk>/',FileDeleteAPIView.as_view()),
    path ('detail/<int:pk>/',FileDetailAPIView.as_view()),
    path ('thumbnail/',FileListThumbNailAPIView.as_view())
]