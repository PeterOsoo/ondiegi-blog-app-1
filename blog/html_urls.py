from django.urls import path

from .views import (
    blog_list_view, 
    create_post_view,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    CategoryListHTMLView,
    CategoryPostsHTMLView,
)

urlpatterns = [
    path('', blog_list_view, name='blog-posts'),  # main blog list
    path('create/', create_post_view, name='create-post'),

    # Category pages
    path('categories/', CategoryListHTMLView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryPostsHTMLView.as_view(), name='category-posts'),

    # Post detail/edit/delete
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='view-post'),
    path('<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='edit-post'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='delete-post'),
]
