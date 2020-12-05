from django.urls import path
from .views import LayoutCreateAPIView, LayoutCatalogListAPIView,SliderListAPIView

urlpatterns = [
    path('layout/', LayoutCreateAPIView.as_view()),
    path('layout_list/<int:page>/', LayoutCatalogListAPIView.as_view()),
    path('sliders/', SliderListAPIView.as_view()),
]
