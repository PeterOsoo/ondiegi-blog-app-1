from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages

from .serializers import RegisterSerializer  
from .forms import CustomUserCreationForm

from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'accounts/home.html')



# ✅ API Registration
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ API Login
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ HTML Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ✅ HTML Login View
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    if request.content_type == 'application/json':
        # API login
        username = request.data.get('username')
        password = request.data.get('password')
    else:
        # HTML login
        username = request.POST.get('username')
        password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        if request.content_type == 'application/json':
            return Response({'token': token.key})
        messages.success(request, 'Logged in successfully ✅')
        return redirect('home')  # ✅ Redirect to a home page (coming up next)

    if request.content_type == 'application/json':
        return Response({'error': 'Invalid credentials'}, status=400)

    return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})


# ✅ HTML Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully ✅')
    return redirect('login')


