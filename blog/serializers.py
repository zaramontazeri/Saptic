from embed_video.backends import detect_backend
from rest_framework import serializers
from rest_framework.fields import Field

from blog.models import Tag, BlogPost, BlogCategory, BlogComment, BlogPostImage

class VideoField(Field):
    def to_representation(self, value):
        my_video = detect_backend(value)
        res = {}
        try:
            res['info'] = my_video.get_info()
        except :
            pass
        try:
            res['code'] = my_video.get_code()
        except :
            pass
        try:
            res["url"] = my_video.get_url()
        except :
            pass
        # try:
        #     res["thumbnail"] = my_video.get_thumbnail_url()
        # except :
        #     pass

        return res

    # def to_internal_value(self, data):
    #     data = data.strip('rgb(').rstrip(')')
    #     red, green, blue = [int(col) for col in data.split(',')]
    #     return "h"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        exclude = ('id',)


class BlogCategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        exclude = ('language',)

    def get_posts_count(self, obj):
        return obj.posts.count()


class BlogCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogComment
        exclude = ('id',)

class BlogPostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostImage
        exclude = ('id',)

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostImage
        exclude = ('id',)

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    category = BlogCategorySerializer()
    comments = serializers.SerializerMethodField()
    video = VideoField()
    gallery_images = serializers.SerializerMethodField()
    # cover = serializers.SerializerMethodField()
    class Meta:
        model = BlogPost
        exclude = ('published', 'priority', 'language', 'author')
    def get_gallery_images(self,instance):
        blog_post = instance.gallery_images.all().order_by("blogimageorder__order")
        return BlogPostImageSerializer(blog_post,many=True).data

    def get_comments(self, obj):
        comments = obj.comments.filter(approved=True).all()
        return BlogCommentSerializer(comments, many=True).data

    # def get_cover(self, obj):
    #     request = self.context.get('request')
        
    #     photo_url = obj.cover.url
    #     return request.build_absolute_uri(photo_url)
