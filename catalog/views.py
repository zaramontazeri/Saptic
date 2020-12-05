from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import LayoutCatalog,Slider
from .serializers import LayoutCatalogSerializer,SliderSerializer


class LayoutCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data["data"]
        # layout = [{"x": i["x"], "y":i["y"], "h":i["h"], "w":i["w"],
        #            'catalog':int(i["catalog"]), "page":int(i["page"])} for i in data]
        # print(layout)
        layout_s = LayoutCatalogSerializer(data=data, many=True)
        is_valid = layout_s.is_valid()
        print(is_valid)
        layout_s.save()
        return Response({"status": "ok"})


class LayoutCatalogListAPIView(ListAPIView):
    def get_queryset(self):
        return LayoutCatalog.objects.filter(page=self.kwargs.get("page"))

    serializer_class = LayoutCatalogSerializer


class SliderListAPIView(ListAPIView):
    def get_queryset(self):
        return Slider.objects.all()

    serializer_class = SliderSerializer
    # Create your views here.
