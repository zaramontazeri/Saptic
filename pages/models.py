from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django_extensions.db import fields as extension_fields

from blog.models import BlogPost, Tag
from asburger import constants
# from tours.models import Tour


class FAQ(models.Model):
    question = models.CharField(max_length=256)
    answer = models.TextField()
    active = models.BooleanField(default=True)
    language = models.CharField(
        max_length=8, choices=constants.LANGUAGE_CHOICES)
    priority = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question

class  Seo (models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=155)
    keywords = models.TextField()
    redirect_add= models.TextField()
    canonical_add =models.TextField()
    ###for having in all models: todo read it.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Page(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(allow_unicode=True,help_text="it works automatically. no need to write yourself!")
    description = models.TextField(blank=True,null=True)
    content = RichTextUploadingField()
    language = models.CharField(
        max_length=8, choices=constants.LANGUAGE_CHOICES)
    active = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to='covers/pages', blank=True, null=True, help_text="1440 * 300 Pixels")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seo  =  GenericRelation('pages.seo')
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=32)
    # phone = models.CharField(max_length=32)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


    def __str__(self):
        return self.email


class CompanyInfo(models.Model):
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    address = models.TextField()
    # point = models.PointField()

    def __str__(self):
        return self.phone



# class TourNewsLetter(models.Model):
#     tour = models.ForeignKey(Tour,on_delete=models.CASCADE)
#     newsletter = models.ForeignKey("NewsLetter",on_delete=models.CASCADE)
#     order = models.PositiveIntegerField(default=0, blank=False, null=False)
#     class Meta(object):
#         ordering = ['order']
#
# class BlogNewsLetter(models.Model):
#     blog = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
#     newsletter = models.ForeignKey("NewsLetter",on_delete=models.CASCADE)
#     order = models.PositiveIntegerField(default=0, blank=False, null=False)
#     class Meta(object):
#         ordering = ['order']

#TODO
# class NewsLetter(models.Model):
#     title = models.CharField(max_length=10)
#     description = models.TextField()
#     cover = models.ImageField(upload_to='covers/newsletter/post', blank=True, null=True)
#     blog = models.ManyToManyField(BlogPost,null=True,blank=True)
#     tour = models.ManyToManyField(Tour,null=True,blank=True)
#     type = models.CharField(max_length=10, choices=(("1","type1"),("2","type2")))
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     sent = models.BooleanField(default=False)
#
#
#


class PromotionalGiftImage(models.Model):
    caption = models.CharField(max_length=128)
    image = models.ImageField(upload_to='covers/gifts/gallery')


class PromotionalGift(models.Model):
    name= models.CharField(max_length=128)
    slug = models.SlugField(allow_unicode=True)
    #todo yeki ham baraye aks balaye safhe bezar
    cover = models.ImageField(upload_to='covers/pages/gifts', blank=True, null=True)
    summary=models.CharField(max_length=250,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    # priority = models.IntegerField() todo
    # video = EmbedVideoField(blank=True, null=True) #todo mikhayn video ham bashe azash?
    gallery_images = models.ManyToManyField("PromotionalGiftImage", blank=True, through="PromotionalGiftImageOrder") #todo order
    related_products = models.ManyToManyField("self", blank=True,null=True ,related_name="similar_products",symmetrical=False) #todo symmertical or not?
    #PRODUCT SPECIFICATIONS is fk to this
    language = models.CharField(
        max_length=8, choices=constants.LANGUAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    seo  =  GenericRelation("pages.seo")


    def __str__(self):
        return self.name

class PromotionalGiftImageOrder(models.Model):
    gift = models.ForeignKey("PromotionalGift",null=True , blank=True,on_delete=models.CASCADE)
    image = models.ForeignKey("PromotionalGiftImage",null=True , blank=True,on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    class Meta(object):
        ordering = ['order']
    def __unicode__(self):
        return self.image.caption


class ProductSpecifications(models.Model):
    specification_key = models.CharField(max_length=128)
    specification_value = models.CharField(max_length=128)
    promotional_gift=models.ForeignKey(PromotionalGift,related_name="specifications",on_delete=models.CASCADE)
    class Meta(object):
        ordering = ['specification_key']


class PageContent(models.Model):

    # Fields
    page_name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='section', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    section = models.CharField(max_length=30)
    cover = models.ImageField(upload_to="upload/images/section_cover")
    title = models.TextField(max_length=100)
    content = models.TextField(max_length=200)
    actions = models.URLField()
    content_type = models.PositiveSmallIntegerField()


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('app_name_pagecontent_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('app_name_pagecontent_update', args=(self.slug,))
