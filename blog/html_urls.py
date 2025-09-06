from django.urls import path

from .views import (
    blog_list_view, 
    create_post_view,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView
)


urlpatterns = [
    path('', blog_list_view, name='blog-posts'),  # 👉 now serves HTML
    path('create/', create_post_view, name='create-post'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='view-post'),
    path('<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='edit-post'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='delete-post'),

]




