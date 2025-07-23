from django.urls import path
from .views import BlogPostListView

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name='blog-posts'),
]
