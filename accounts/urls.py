from django.urls import path
from .views import register_user, login_user, register_view, login_view

urlpatterns = [
    path('register-api/', register_user, name='api-register'),
    path('login-api/', login_user, name='api-login'),
    path('register/', register_view, name='register'), # HTML view
    path('login/', login_view, name='login'), # HTML view


]
