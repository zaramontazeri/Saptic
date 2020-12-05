from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from rangefilter.filter import DateRangeFilter

from blog.models import Tag, BlogCategory, BlogPost, BlogComment, BlogPostImage
from pages.admin import RelatedSeoAdmin


class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'language')
    prepopulated_fields = {'slug': ('title',)}

class BlogImageAdmin(SortableInlineAdminMixin,admin.TabularInline):
    model=BlogPost.gallery_images.through
    list_display = ('order')
    list_display_links = ()



class BlogPostAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('title', 'slider', 'published', 'priority', 'author',
                    'category', 'language')
    list_filter = ('slider', 'published', 'priority', 'author', 'category')
    list_editable = ('slider', 'published', 'priority')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogImageAdmin,RelatedSeoAdmin]




class BlogCommentAdmin(admin.ModelAdmin):
    list_filter = (
        'approved',
        ('created_at', DateRangeFilter),
    )
    list_display = ('text', 'approved', 'post', 'created_at')


admin.site.register(Tag, TagAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
admin.site.register(BlogPostImage)

