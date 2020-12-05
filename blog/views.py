from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from blog.filterset import MyFilterBackend, BlogListFilter
from blog.models import BlogCategory, BlogPost, BlogComment
from blog.serializers import BlogCategorySerializer, BlogPostSerializer, BlogCommentSerializer
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.views import FlatMultipleModelAPIView

from datetime import datetime
import collections


# temporary coments #todo
# from tours.filterset import TourListFilter
# from tours.serializers import TourSerializer
# from tours.models import Tour


class BlogCategoryList(generics.ListAPIView):
    """
    List Blog Categories
    """
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()
    authentication_classes = []

    def list(self, request):
        language = request.query_params.get('LANGUAGE_CODE', 'en')
        categories = self.queryset.filter(language=language).all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)


class BlogPostByCategoryList(generics.ListAPIView):
    """
    List Blog Posts by Category
    """
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    authentication_classes = []

    def list(self, request, category_id, format=None):
        per_page = int(request.query_params.get('per_page', 10))
        page = int(request.query_params.get('page', 1))

        category = get_object_or_404(BlogCategory, pk=category_id)
        language = request.query_params.get('lang', 'en')
        posts = category.posts.filter(
            language=language, published=True).order_by('-created_at').all()
        paginator = Paginator(posts, per_page)
        return Response(BlogPostSerializer(paginator.page(page), many=True).data)


class BlogPostList(generics.ListAPIView):
    """
    List Blog Posts
    """
    authentication_classes = []

    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    filter_backends = [ MyFilterBackend]
    filter_class = BlogListFilter

    def list(self, request, format=None):
        '''

        :param request:
        :param format:
        :return:
        '''
        per_page = int(request.query_params.get('per_page', 10))
        page = int(request.query_params.get('page', 1))
        language = request.query_params.get('lang', 'fa')
        if 'search' in request.query_params:
            posts = BlogPost.objects.filter(
                language=language,
                published=True,
                title__icontains=request.query_params['search']
            ).order_by("-priority")
        else:
            posts = BlogPost.objects.filter(
                language=language, published=True).order_by("-priority")
        paginator = Paginator(posts, per_page)
        context = self.get_serializer_context()
        return Response(BlogPostSerializer(paginator.page(page),context=context, many=True,).data )


# def title_without_letter(queryset, request, *args, **kwargs):
#     letter_to_exclude = request.query_params['letter']
#     return queryset.exclude(title__icontains=letter_to_exclude)

def title_search(queryset, request, *args, **kwargs):
    search = request.query_params['search']
    return queryset.filter(title__icontains=search)


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 2


# todo should I change it to sth useful in this project?
# class BlogTourList( ObjectMultipleModelAPIView):
#     authentication_classes = []
#
#     pagination_class = LimitPagination
#     # filter_backends = (filters.SearchFilter,)
#     # search_fields = ('title',)
#     def get_querylist(self):
#         # title = self.request.query_params['play'].replace('-',' ')
#
#         querylist = (
#             {'queryset': BlogPost.objects.all(), 'serializer_class': BlogPostSerializer,'filter_fn': title_search},
#             {'queryset': Tour.objects.all(), 'serializer_class': TourSerializer,'filter_fn': title_search},
#         )
#
#         return querylist
#     def list(self, request, *args, **kwargs):
#         querylist = self.get_querylist()
#         results = self.get_empty_results()
#         for query_data in querylist:
#             self.check_query_data(query_data)
#             queryset = self.load_queryset(query_data, request, *args, **kwargs)
#             # Run the paired serializer
#             context = self.get_serializer_context()
#             data = query_data['serializer_class'](queryset, many=True, context=context).data
#             typee = type(data)
#             try:
#                 if   data['type'] ==  "FeatureCollection":
#                     data = data['features']
#             except:
#                 pass
#             label = self.get_label(queryset, query_data)
#             # Add the serializer data to the running results tally
#             results = self.add_to_results(data, label, results)
#         formatted_results = self.format_results(results, request)
#         if self.is_paginated:
#             try:
#                 formatted_results = self.paginator.format_response(formatted_results)
#             except AttributeError:
#                 raise NotImplementedError(
#                     "{} cannot use the regular Rest Framework or Django paginators as is. "
#                     "Use one of the included paginators from `drf_multiple_models.pagination "
#                     "or subclass a paginator to add the `format_response` method."
#                     "".format(self.__class__.__name__)
#                 )
#         return Response(formatted_results)

    # def get(self,request):
    #     per_page = int(request.query_params.get('per_page', 10))
    #     page = int(request.query_params.get('page', 1))
    #     language = request.query_params.get('LANGUAGE_CODE', 'en')
    #     slider = bool(request.query_params.get('slider', True))
    #     if 'search' in request.query_params:
    #         posts = BlogPost.objects.filter(
    #             language=language,
    #             published=True,
    #             title__icontains=request.query_params['search'],
    #             slider=slider
    #         ).order_by('-created_at')
    #         tours = Tour.objects.filter(
    #             guide_languages__language=language,
    #             active=True, active_until__gt=datetime.now(),
    #             title__icontains=request.query_params['search'],
    #             slideshow=slider
    #         ).order_by('-created_at')
    #     else:
    #         posts = BlogPost.objects.filter(language=language, published=True,slider=slider).order_by('-created_at')
    #         tours = Tour.objects.filter(guide_languages__language=language,active=True, active_until__gt=datetime.now(),slideshow=slider).order_by('-created_at')
    #         # tours=Tour.objects.all()
    #     posts_serializer = BlogPostSerializer(posts,many=True)
    #     tours_serializer = TourSerializer(tours,many=True)
    #     posts_list= list(posts_serializer.data)
    #     tours_list = list(tours_serializer.data["features"])
    #     tours_list  = [{**dict(i),"created_at":i["properties"]["created_at"]} for i in tours_list]
    #     all_list = posts_list + tours_list
    #     all_list_dict = [ dict(i) for i in all_list]
    #     newlist = sorted(all_list_dict,key = lambda i: i['created_at'],reverse=True )
    #     paginator = Paginator(newlist, per_page)
    #     p = paginator.page(page)
    #     return Response({"list":p.object_list})

class BlogPostTypeList(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    authentication_classes = []

    def list(self, request, post_type, format=None):
        per_page = int(request.query_params.get('per_page', 10))
        page = int(request.query_params.get('page', 1))
        language = request.query_params.get('LANGUAGE_CODE', 'en')
        posts = BlogPost.objects.filter(
            language=language, published=True, post_type=post_type).order_by('-created_at').all()
        paginator = Paginator(posts, per_page)
        return Response(BlogPostSerializer(paginator.page(page), many=True).data)


class RelatedBlogPostList(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    authentication_classes = []

    def list(self, request, post_id):
        per_page = int(request.query_params.get('per_page', 10))
        page = int(request.query_params.get('page', 1))
        language = request.query_params.get('LANGUAGE_CODE', 'en')
        post_type = BlogPost.objects.get(pk=post_id).post_type
        posts = BlogPost.objects.filter(language=language, published=True, post_type=post_type).order_by(
            '-created_at').all()

        paginator = Paginator(posts, per_page)
        return Response(BlogPostSerializer(paginator.page(page), many=True).data)


class BlogPostDetail(generics.RetrieveAPIView):
    """
    Get Blog Post detail
    """
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.filter(published=True)
    authentication_classes = []

    def list(self, request):
        language = request.query_params.get('LANGUAGE_CODE', 'en')
        posts = self.queryset.filter(language=language).all()
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)


class BlogPostSliderList(generics.ListAPIView):
    """
    Get Blog Post Sliders
    """
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.filter(published=True, slider=True)
    authentication_classes = []

    def list(self, request):
        language = request.query_params.get('LANGUAGE_CODE', 'en')
        posts = self.queryset.filter(language=language)
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)


class BlogComment(generics.CreateAPIView):
    """
    Create Comment on Post
    """
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = BlogCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
