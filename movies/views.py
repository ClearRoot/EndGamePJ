from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .forms import MovieForm, PeopleForm, MovieRankForm, CommentForm, ScoreForm
from .models import Genre, Movie, MovieRank, People, Comment, Score
from .crawling import movie_data
import json

# Create your views here.
@login_required
def list(request):
    if request.user.is_authenticated:
        return render(request, 'movies/list.html')
    #else일때
    return render(request, 'movies/main.html')
        
@login_required
def json_list(request):
    movies = Movie.objects.all()
    scores = Score.objects.filter(user=request.user).all()
    movies_json = serializers.serialize('json', movies)
    scores_json = serializers.serialize('json', scores)
    # return JsonResponse(json.dumps(movies_json, ensure_ascii=False), safe=False)
    return JsonResponse({'movies_json':movies_json, 'scores_json':scores_json, 'user_id':request.user.id}, content_type='application/json; charset=utf-8')

@login_required
def detail(request, movie_id):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_id)
        comment_form = CommentForm()
    return render(request, 'movies/detail.html', {'movie':movie, 'comment_form':comment_form})

@login_required
def comment_create(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            return redirect('movies:detail', movie_id)

@login_required
def comment_update(request, movie_id, comment_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user:
        if request.method == "POST":
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.save()
        else:
            comment_form = CommentForm(instance=comment)
            return render(request, 'movies/detail.html', {'movie':movie, 'comment_form':comment_form})
    #잘못된 접근이므로 Error처리해주는게 옳음
    return redirect('movies:detail', movie_id)

@login_required
def comment_delete(request, movie_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user == request.user:
        comment.delete()
        return redirect('movies:detail', movie_id)
    #잘못된 접근이므로 Error처리해주는게 옳음
    return redirect('movies:detail', movie_id)

@login_required
def score_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    is_res = False
    if request.method == "GET":
        user = request.user
        value = int(request.GET.get('value'))
        score = Score.objects.create(movie=movie, user=user, value=value)
        is_res = True
        # score_form = ScoreForm(request.POST)
        # if score_form.is_valid():
        #     score = score_form.save(commit=False)
        #     score.movie = movie
        #     score.user = request.user
        #     score.save()
        #     is_res = True
        #     score_id = score.id
    return JsonResponse({'is_res':is_res, 'score_id':score.id})

# @login_required
# def score_update(request, movie_id, score_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
#     score = get_object_or_404(Score, pk=score_id)
#     if request.user == score.user:
#         if request.method == "POST":
#             score_form = ScoreForm(request.POST, instance=score)
#             if score_form.is_valid():
#                 score = score_form.save(commit=False)
#                 score.save()
#         else:
#             score_form = ScoreForm(instance=comment)
#             return render(request, 'movies/detail.html', {'movie':movie, 'score_form':score_form})
#     #잘못된 접근이므로 Error처리해주는게 옳음
#     return redirect('movies:detail', movie_id)

@login_required
def score_delete(request, movie_id, score_id):
    score = get_object_or_404(Score, pk=score_id)
    is_res = False
    if score.user == request.user:
        score.delete()
        is_res = True
        return JsonResponse({'is_res':is_res})

"""Admin"""
@login_required
def crawling(request):
    if request.user.is_superuser:
        admin = request.user
        movie_data()
        return render(request, 'movies/crawling.html', {'admin':admin})
    return redirect('movies:list')

@login_required
def update(request, movie_id):
    if request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=movie_id)
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                movie = form.save(commit=False)
                movie.save()
                return redirect('movies:detail', movie_id)
        else:
            form = MovieForm(instance=movie)
        return render(request, 'movies/form.html', {'form':form})
    return redirect('movies:list')

@login_required
def delete(request, movie_id):
    if request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
    return redirect('movies:list')