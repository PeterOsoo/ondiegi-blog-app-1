from django.urls import path
from .views import BlogPostListView, CreateBlogPostView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='api-posts'),
    path('create/', CreateBlogPostView.as_view(), name='api-create-post'),
]
