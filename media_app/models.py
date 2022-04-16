from django.db import models

from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import exception_handler
User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.phone, filename)

class File(models.Model):
    file = models.FileField(blank=False, null=False,upload_to=user_directory_path)
    user = models.ForeignKey(User ,on_delete=CASCADE )
    name = models.CharField(max_length=100 )
    alt = models.CharField(max_length=100,null=True,blank=True)
    caption = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.file.url


