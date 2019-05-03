from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .froms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/form.html', {'form':form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/form.html', {'form':form})

def logout(request):
    auth_logout(request)
    return redirect('movies:list')