from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('movies:list')
        else:
            form = CustomUserCreationForm()
        return render(request, 'accounts/form.html', {'form':form})
    else:
        return redirect('movies:list')

def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('movies:list')
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/form.html', {'form':form})
    else:
        return redirect('movies:list')

@ login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:list')

@ login_required
def user_page(request, id):
    User = get_user_model()
    user_info = User.objects.get(id=id)
    return render(request, "accounts/user_page.html", {'user_info':user_info})

@ login_required
def follow(request, id):
    User = get_user_model()
    me = request.user
    you = User.objects.get(id=id)

    if me != you:
        if you in me.followings.all():
            me.followings.remove(you)
            is_follow = False
        else:
            me.followings.add(you)
            is_follow = True
    return JsonResponse({'is_follow':is_follow, 'followers_count':you.followers.count()})

@ login_required
def edit_profile(request, id):
    User = get_user_model()
    user = User.objects.get(id=id)
    me = request.user
    if me == user:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('accounts:user_page', id)
        else:
            form = CustomUserChangeForm(instance=user)
        return render(request, 'accounts/form.html', {'form':form})
    return redirect('movies:list')
    