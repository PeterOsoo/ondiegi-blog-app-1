from django.urls import path
from .views import BlogPostListView, register_user, login_user


urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog-posts'),
    path('register/', register_user, name='register'), 
    path('login/', login_user, name='login'),

]
