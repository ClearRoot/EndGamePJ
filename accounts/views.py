from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from .forms import CustomUserCreationForm, CustomUserPasswordForm, CustomUserChangeForm
from movies.models import Movie

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

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:list')

@login_required
def user_page(request, user_id):
    User = get_user_model()
    user_info = get_object_or_404(User, pk=user_id)
    return render(request, "accounts/user_page.html", {'user_info':user_info})

@login_required
def edit_profile(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    me = request.user
    if me == user:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('accounts:user_page', user_id)
        else:
            form = CustomUserChangeForm(instance=user)
        return render(request, 'accounts/form.html', {'form':form})
    return redirect('movies:list')
    
@login_required
def password_enter_form(request):
    user = request.user
    if request.method == 'POST':
        pwd = request.POST.get('pwd')
        if check_password(pwd, user.password):
            # if request.POST.get('com') == 'leave':
            #     return redirect('accounts:leaving_user', user.id)
            # elif request.POST.get('com') == 'update':
            #     return redirect('accounts:edit_profile', user.id)
            # else:
            #     #잘못된접근 에러처리
            #     return redirect('movies:list')
            return check_password(pwd, user.password)
    else:
        com = 'leaving_user'
    return render(request, 'accounts/password_form.html', {'com':com})
    
@login_required
def follow(request, user_id):
    User = get_user_model()
    me = request.user
    you = get_object_or_404(User, pk=user_id)

    if me != you:
        if you in me.followings.all():
            me.followings.remove(you)
            is_follow = False
        else:
            me.followings.add(you)
            is_follow = True
    return JsonResponse({'is_follow':is_follow, 'follows_count':you.followers.count(), 'followings_count':you.followings.count()})

    
@login_required
def leaving_user(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    if user == request.user:
        user.delete()
        return redirect('movies:list')
    #에러처리해야하는 요소
    return redirect('movies:list')

@login_required        
def pickup(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    if movie in user.pick_movie.all():
        user.pick_movie.remove(movie)
        is_pickup = False
    else:
        user.pick_movie.add(movie)
        is_pickup = True
    return JsonResponse({'is_pickup':is_pickup, 'pick_user_count':movie.pick_user.count(), 'pick_movie_count':user.pick_movie.count()})