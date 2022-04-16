from django.contrib import admin
from media_app.models import File
class FileAdmin(admin.ModelAdmin):

    list_display = ('caption',)


admin.site.register(File, FileAdmin)
# Register your models here.
