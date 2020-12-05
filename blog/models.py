from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from embed_video.fields import EmbedVideoField

from partak import constants

from django.contrib.auth import get_user_model
User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class BlogPostImage(models.Model):
    caption = models.CharField(max_length=128)
    image = models.ImageField(upload_to='covers/blog/gallery')


class BlogImageOrder(models.Model):
    blog = models.ForeignKey("BlogPost", null=True,
                             blank=True, on_delete=models.CASCADE)
    image = models.ForeignKey(
        "BlogPostImage", null=True, blank=True, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta(object):
        ordering = ['order']

    def __str__(self):
        return self.image.caption


class BlogCategory(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(allow_unicode=True)
    cover = models.ImageField(
        upload_to='covers/blog/category', blank=True, null=True)
    language = models.CharField(
        max_length=8, choices=constants.LANGUAGE_CHOICES)

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    POST_TYPE_CHOICES = [
        ('post', 'Post'),
        ('video', 'Video'),
        ('gallery', 'Image Gallery'),
    ]
    title = models.CharField(max_length=128)
    slug = models.SlugField(
        allow_unicode=True, help_text="it works automatically. no need to write yourself!")
    content = RichTextUploadingField()
    summary = models.TextField(blank=True, null=True)
    slider = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    priority = models.IntegerField()
    cover = models.ImageField(
        upload_to='covers/blog/post', blank=True, null=True)
    # post_type = models.CharField(max_length=16, choices=POST_TYPE_CHOICES)
    video = EmbedVideoField(blank=True, null=True)
    gallery_images = models.ManyToManyField(
        BlogPostImage, blank=True, through="BlogImageOrder")
    language = models.CharField(
        max_length=8, choices=constants.LANGUAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE,
                                 related_name='posts')
    tags = models.ManyToManyField(Tag)
    seo = GenericRelation("pages.seo")

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')

    class Meta:
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'
        unique_together = ('post', 'user')

    def __str__(self):
        return self.text
