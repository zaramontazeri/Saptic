from django.urls import path

from blog import views

urlpatterns = [
    # todo is the error ok? bcuz in the 3d one it does not make error
    path('related/<int:post_id>/', views.RelatedBlogPostList.as_view()),
    path('categories/', views.BlogCategoryList.as_view()),
    path('posts/category/<int:category_id>/',
         views.BlogPostByCategoryList.as_view()),
    path('posts/', views.BlogPostList.as_view(), name='posts'),
    path('posts/type/<str:post_type>/', views.BlogPostTypeList.as_view()),
    path('post/<int:pk>/', views.BlogPostDetail.as_view()),
    path('posts/sliders/', views.BlogPostSliderList.as_view()),
    # path('posts_tours/', views.BlogTourList.as_view()),  # todo change to what?
    path('comments/', views.BlogComment.as_view()),
]
