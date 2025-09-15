from django.urls import path
from .views import BlogPostListView, CreateBlogPostView, CategoryListView, CategoryListCreateView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='api-posts'),
    path('create/', CreateBlogPostView.as_view(), name='api-create-post'),
    path("categories/", CategoryListView.as_view(), name="api-categories"),
    path("api/categories/", CategoryListCreateView.as_view(), name="api-category-list"),

]
