from django.contrib import admin
from .models import Catalog, PageLayout, LayoutCatalog,Slider
# Register your models here.


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ["name", 'description', 'image']


@admin.register(PageLayout)
class LayoutAdmin(admin.ModelAdmin):
    change_form_template = 'admin/test.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        print(object_id)
        try:
            obj_id = int(object_id)
            extra_context = extra_context or {}
            catalogs = Catalog.objects.all()
            print(obj_id)
            catalog_layout = LayoutCatalog.objects.filter(page__id=obj_id)
            extra_context["catalogs"] = catalogs
            extra_context["layout_id"] = object_id
            extra_context["catalog_layout"] = catalog_layout
        except:
            pass
        return super(LayoutAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ["description", 'image']