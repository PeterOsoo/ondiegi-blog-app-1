from django.urls import path
from .views import register_user, login_user, register_view, login_view, logout_view, profile_view

urlpatterns = [
    path('login/', login_view, name='login'), # HTML view
    path('register/', register_view, name='register'), # HTML view
    path('logout/', logout_view, name='logout'),
    path('register-api/', register_user, name='api-register'),
    path('login-api/', login_user, name='api-login'),
    path('profile/', profile_view, name='profile'),  # ✅ Add this

]
