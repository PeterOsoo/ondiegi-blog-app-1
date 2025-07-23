from django.urls import path
from .views import register_user, login_user, register_view, login_view, logout_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'), # HTML view
    path('register/', register_view, name='register'), # HTML view
    path('logout/', logout_view, name='logout'),
    path('register-api/', register_user, name='api-register'),
    path('login-api/', login_user, name='api-login'),


]
