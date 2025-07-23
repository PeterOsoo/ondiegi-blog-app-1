from django.urls import path
from .views import BlogPostListView, register_user


urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog-posts'),
    path('register/', register_user, name='register'),  # 👈 New line
]
