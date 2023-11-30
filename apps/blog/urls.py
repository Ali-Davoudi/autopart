from django.urls import path

from . import views

urlpatterns = [
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/category/<category>/', views.BlogListView.as_view(), name='blog_list_by_category'),
    path('blog/tag/<tag>/', views.BlogListView.as_view(), name='blog_list_by_tag'),
    path('blog/<pk>/<name>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/articles/', views.SearchBlogView.as_view(), name='search_blog'),
    path('blog/add-blog-comment/', views.AddBlogComment.as_view(), name='add_blog_comment'),
]
