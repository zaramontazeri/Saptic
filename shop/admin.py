from django.contrib import admin
from django.forms import ModelForm,ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from nested_inline.admin import NestedStackedInline,NestedTabularInline, NestedModelAdmin
from shop.models import (
    Shop,
    Product,
    ProductGalleryImage,
    ProductVariation,
    ProductVariationAttribute,
    ProductAttribute,
    ProductReview,
    OrderedItem,
    Transactions,
    Invoice,
    DiscountCode,
    WorkingTime,
    OccasionalDiscount,
    Category,
    Subcategory)
# Register your models here.



class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline,
    ]
    prepopulated_fields = {'slug': ('title',)}

class WorkingTimeInline(admin.TabularInline):
    model = WorkingTime

class ShopAdmin(admin.ModelAdmin):
    inlines = [
        # MenuitemInline,
        WorkingTimeInline
    ]
    prepopulated_fields = {'slug': ('title',)}


##################################################
class ProductGalleryImageInline(NestedTabularInline):#admin.TabularInline
    model = ProductGalleryImage
    extra = 3

class ProductVariationAttributeInline(NestedTabularInline):
    model = ProductVariation.specifications.through


class ProductVariationInline(NestedStackedInline):#admin.StackedInline
    model = ProductVariation
    extra = 2
    readonly_fields = ["occasional_discount"] #BIG TODO : make an occasional_discount table
    #todo just add this in table and be read only here? or let them alter from this one too?
    # filter_horizontal = ('specifications',)
    exclude = ('specifications',)
    inlines = [
        # ProductGalleryImageInline,
        ProductVariationAttributeInline,
    ]

class ProductAdmin(NestedModelAdmin):
    model = Product
    list_display = ['title']
    search_fields = ['title'] # "menuitem__title","menuitem__category__title" if you want to search on menuitem and category cuz it's FK
    inlines = [
        ProductGalleryImageInline,
        ProductVariationInline,
    ]

class ProductReviewAdmin(admin.ModelAdmin):
    model=ProductReview
    list_display = ['product','created_at','confirmed']
    list_editable = ['confirmed']
    list_filter = ['confirmed']
###################################################

class OrderedItemInline(admin.TabularInline): #TODO if you dont want to make it read only later you have to work on having effect on total price
    model = OrderedItem

class TransactionsInline(admin.TabularInline): #TODO BIG TODO LATER MAKE THIS COMPLETELY READ_ONLY
    model = Transactions


class InvoiceAdmin(admin.ModelAdmin): #todo later make some things read_only
    inlines = [OrderedItemInline,TransactionsInline]

##############################################
class DiscountCodeAdmin(admin.ModelAdmin): #TODO signal too tour hast bara inke khodesh tolid kone
    list_display = ['code','percentage','expire_at']


class OccasionalDiscountAdminForm(ModelForm): #link:https://stackoverflow.com/questions/18505266/django-admin-select-reverse-foreign-key-relationships-not-create-i-want-to-a
    products = ModelMultipleChoiceField(
        queryset=ProductVariation.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='products', is_stacked=False))

    class Meta:
        model = OccasionalDiscount
        fields = '__all__'# ['title','percentage']

    def __init__(self, *args, **kwargs):
        super(OccasionalDiscountAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            # fill initial related values
            self.fields['products'].initial = self.instance.occasional_discount_set.all()

class OccasionalDiscountAdmin(admin.ModelAdmin):
   form = OccasionalDiscountAdminForm

   def save_model(self, request, obj, form, change):
       original_products = obj.occasional_discount_set.all()
       new_products = form.cleaned_data['products']
       remove_qs = original_products.exclude(id__in=new_products.values('id'))
       add_qs = new_products.exclude(id__in=original_products.values('id'))
       obj.save()
       for item in remove_qs:
           obj.occasional_discount_set.remove(item)

       for item in add_qs:
           # obj.occasional_discount_set.add(item)
           item.occasional_discount = obj
           item.save()
       # obj.save()





admin.site.register(Shop,ShopAdmin)
admin.site.register(Product,ProductAdmin)
# admin.site.register(ProductVariationAttribute,ProductVariationAttributeAdmin)
admin.site.register(ProductAttribute)
admin.site.register(ProductReview,ProductReviewAdmin)

admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(DiscountCode,DiscountCodeAdmin)
admin.site.register(OccasionalDiscount,OccasionalDiscountAdmin)
