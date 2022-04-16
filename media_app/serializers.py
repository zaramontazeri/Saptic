from django.db.models.fields.reverse_related import ManyToManyRel, ManyToOneRel
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField 
from .models import File
from easy_thumbnails.files import get_thumbnailer
import magic
#   "id": 4,
#   "size": 40484,
#   "mime_type": "image/jpeg",
#   "file": "http://localhost:8060/uploads/user_09132693958/156343933.jpg",
#   "name": "دانشگاه صنعتی اصفهان",
#   "alt": "iut-isf",
#   "caption": "تصویر سردر دانشگاه صنعتی اصفهان",
#   "user": 1
class FileSerializer(serializers.ModelSerializer):

    size = SerializerMethodField()
    mime_type = SerializerMethodField()
    # usages = SerializerMethodField()
    class Meta:
        model = File
        fields = "__all__"
    
    def get_size(self,instance):
        return instance.file.size
    def get_mime_type(self,instance):
        a = instance.file.file.read(1024)
        instance.file.file.close()
        b = magic.from_buffer(a, mime=True)
        return b
        # return instance.file.

class FileThumbnailSerializer(serializers.ModelSerializer):

    thumb_nail_100_100 = SerializerMethodField()
    thumb_nail_50_50 = SerializerMethodField()
    # mime_type = SerializerMethodField()
    # usages = SerializerMethodField()
    class Meta:
        model = File
        fields = ["thumb_nail_100_100","thumb_nail_50_50"]
    
    def get_thumb_nail_100_100(self,instance):
        options = {'size': (100, 100), 'crop': True}
        request  = self.context.get('request', None)
        thumb_url = get_thumbnailer(instance.file).get_thumbnail(options).url
        if request:
            thumb_url=request.build_absolute_uri(thumb_url)
        return thumb_url
    def get_thumb_nail_50_50(self,instance):
        options = {'size': (50, 50), 'crop': True}
        request  = self.context.get('request', None)
        thumb_url = get_thumbnailer(instance.file).get_thumbnail(options).url
        if request:
            thumb_url=request.build_absolute_uri(thumb_url)
        return thumb_url

class FileDetailSerializer(serializers.ModelSerializer):

    size = SerializerMethodField()
    mime_type = SerializerMethodField()
    usages = SerializerMethodField()
    class Meta:
        model = File
        fields = "__all__"
    
    def get_size(self,instance):
        return instance.file.size
    def get_mime_type(self,instance):
        return magic.from_buffer(instance.file.file.read(1024), mime=True)
        # return instance.file.
    def get_usages (self,instance):
        fields = instance._meta.get_fields()
        rels = [i for i in fields if isinstance(i, ManyToOneRel) or isinstance(i,ManyToManyRel)]
        res = []
        for i in rels:
            related_name = i.related_name
            # print(i.field,i.related_name,i.related_model,i.get_related_field())
            if related_name ==None:
                related_name =str( i.related_model.__name__).lower()+"_set"
            # print ([(str(j),i.field) for j in list(getattr(instance,related_name).all())])
            res = res+[(str(j),i.related_model.__name__) for j in list(getattr(instance,related_name).all())]
        return res

class FileSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        read_only_fields = ['file','user','name','alt','caption']

class FileRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return File.objects.all()

    def to_representation(self, instance):
        request  = self.context.get('request', None)
        # thumb_50_url = get_thumbnailer(instance.file).get_thumbnail({'size': (50, 50), 'crop': True}).url
        # thumb_100_url = get_thumbnailer(instance.file).get_thumbnail({'size': (100, 100), 'crop': True}).url
        thumb_50_url = instance.file.url
        thumb_100_url = instance.file.url

        if request:
            thumb_50_url=request.build_absolute_uri(thumb_50_url)
            thumb_100_url=request.build_absolute_uri(thumb_100_url)

        request  = self.context.get('request', None)
        if request:
            return {'id':instance.id,'file':request.build_absolute_uri(instance.file.url), 
            'name':instance.name, 'alt':instance.alt, 'caption':instance.caption,
            "thumb_nail_50_50":thumb_50_url,"thumb_nail_100_100":thumb_100_url,
             }
        else :
            return {'id':instance.id,'file':instance.file.url, 
            'name':instance.name, 'alt':instance.alt, 'caption':instance.caption,
            "thumb_nail_50_50":thumb_50_url,"thumb_nail_100_100":thumb_100_url,
             }

    def to_internal_value(self, data):
        # name = data.get('name', None)
        # inventor = data.get('inventor', None)
        id = data
        if not isinstance(data ,File):
            return File.objects.get(pk=id)
        else :
            return data


            