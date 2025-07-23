from django.urls import path
from .views import BlogPostListView, CreateBlogPostView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog-posts'),
    path('create/', CreateBlogPostView.as_view(), name='create-post'),
]
