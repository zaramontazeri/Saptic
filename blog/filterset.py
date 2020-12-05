import decimal

import rest_framework_filters as filters
from django.db.models import Min, F, Count, Q
from django.utils.datetime_safe import date,datetime
from rest_framework_filters.backends import RestFrameworkFilterBackend

from blog.models import BlogPost, BlogCategory



class BlogOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
        ]
    def filter(self, qs, value):
        return super().filter(qs, value)

class MyFilterBackend(RestFrameworkFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs

class BlogCategoryFilter(filters.FilterSet):
    class Meta:
        model = BlogCategory
        fields = {'title': ['exact', 'in', 'startswith']}


class BlogListFilter(filters.FilterSet):
    category = filters.RelatedFilter(BlogCategoryFilter, field_name='category', queryset=BlogCategory.objects.all())
    ordering = BlogOrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('priority', 'priority'),
        ),
    )
    class Meta:
        model = BlogPost
        fields={"priority":["lte",'gte',"exact"],}
