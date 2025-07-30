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
    path('<int:pk>/', BlogPostDetailView.as_view(), name='view-post'),
    path('<int:pk>/edit/', BlogPostUpdateView.as_view(), name='edit-post'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='delete-post'),

]




