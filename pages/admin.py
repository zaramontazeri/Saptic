from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
# from django.contrib.gis import admin
from django.contrib import admin
# from leaflet.admin import LeafletGeoAdmin
from rangefilter.filter import DateRangeFilter

from pages.models import FAQ, Page, ContactMessage, Subscription, CompanyInfo, Seo, PromotionalGift, \
    ProductSpecifications, PromotionalGiftImage


# from pages.serializers import NewsLetterSerializer
# from pages.tasks import send_newsletter_email_task
# from asburger.celery import debug_task

class RelatedSeoAdmin(GenericStackedInline):
    model=Seo

    list_display = ('order','title',
    'description',
    'keywords',
    'redirect_add',
    'canonical_add'
    )
    extra = 1
    # ct_field = 'content_type'
    # ct_fk_field = "content_object"

class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'active', 'language', 'priority')
    list_editable = ('active', 'priority')
    list_filter = ('active', 'language', 'priority')


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'active', 'created_at')
    list_editable = ('active',)
    list_filter = ('active',)
    prepopulated_fields = {'slug': ('title',), }
    inlines = [RelatedSeoAdmin]


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter = (
    	('created_at', DateRangeFilter),
    )
# class NewsLetterAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'type','created_at')
#     list_filter = (
#     	('created_at', DateRangeFilter),
#     )
#     actions = ['send_news_letter',]
#
#     def send_news_letter(self, request, queryset):
#         news_serializer = NewsLetterSerializer(queryset,many=True)
#         print(news_serializer.data)
#
#         send_newsletter_email_task.delay(news_serializer.data)
#         # debug_task.delay()
#         print("dssdf")
#
#
#     send_news_letter.short_description = 'send selected newsletter for subscription'
class ProductSpecificationsAdmin(admin.TabularInline): # todo SortableInlineAdminMixin?
    model = ProductSpecifications
    fk_name = "promotional_gift"
    list_display = ('specification_key','specification_value')
    list_display_links = ()
#ProductSpecifications
#related products

class PromotionalGiftImageAdmin(SortableInlineAdminMixin,admin.TabularInline):#GenericStackedInline
    model=PromotionalGift.gallery_images.through
    list_display = ('image','caption','order')
    # list_display = ('order')
    list_display_links = ()

#todo complete it
class PromotionalGiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'created_at')
    list_filter = ('language',)
    prepopulated_fields = {'slug': ('name',), }
    inlines = [PromotionalGiftImageAdmin,ProductSpecificationsAdmin, RelatedSeoAdmin]


admin.site.register(PromotionalGift,PromotionalGiftAdmin)
admin.site.register(PromotionalGiftImage)
admin.site.register(FAQ, FaqAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Subscription)
# admin.site.register(CompanyInfo, LeafletGeoAdmin)
# admin.site.register(NewsLetter, NewsLetterAdmin)
from django.contrib import admin
from django import forms
from .models import PageContent

class PageContentAdminForm(forms.ModelForm):

    class Meta:
        model = PageContent
        fields = '__all__'


class PageContentAdmin(admin.ModelAdmin):
    form = PageContentAdminForm
    list_display = ['page_name', 'slug', 'created', 'last_updated', 'section', 'cover', 'title', 'content', 'actions', 'content_type']
    readonly_fields = [ 'created', 'last_updated']

admin.site.register(PageContent, PageContentAdmin)