from django.urls import path
from .views import BlogPostListView, CreateBlogPostView, create_post_view, blog_list_view, BlogPostDetailView

urlpatterns = [
    path('', blog_list_view, name='blog-posts'),  # 👉 now serves HTML
    path('create/', create_post_view, name='create-post'),
    path('api/create/', CreateBlogPostView.as_view(), name='api-create-post'),
    path('api/posts/', BlogPostListView.as_view(), name='api-posts'),  # 👉 moved here
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='view-post'),
]

# DO NOT USE THIS FILE FOR API ENDPOINTS OR HTML VIEWS
# Use blog/api_urls.py for API endpoints and blog/urls.py for HTML views.