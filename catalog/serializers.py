from rest_framework import serializers
from .models import LayoutCatalog, PageLayout, Catalog, Slider


class LayoutCatalogListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        cp = [{"c_id": i["catalog"].id, "p_id":i["page"].id}
              for i in validated_data]
        cpp = [dict(t) for t in {tuple(d.items()) for d in cp}]
        print(cpp)
        for i in cpp:
            f = LayoutCatalog.objects.filter(
                catalog=i["c_id"], page=i["p_id"]).delete()
        layouts = [LayoutCatalog(**item) for item in validated_data]
        return LayoutCatalog.objects.bulk_create(layouts)
class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = "__all__"
        list_serializer_class = LayoutCatalogListSerializer


class LayoutCatalogSerializer(serializers.ModelSerializer):
    catalog_obj = serializers.SerializerMethodField()

    def get_catalog_obj(self, obj):
        catalog = obj.catalog
        return CatalogSerializer(catalog).data

    class Meta:
        model = LayoutCatalog
        fields = ('catalog', 'page', 'x', 'y',
                  'w', 'h', 'el_id', 'catalog_obj')
        list_serializer_class = LayoutCatalogListSerializer

    def create(self, validated_data):
        print(validated_data)
        return LayoutCatalog.objects.create(**validated_data)

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = "__all__"
