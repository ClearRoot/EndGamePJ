from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovieForm, PeopleForm, MovieRankForm, CommentForm, ScoreForm, MovieDipForm
from .models import Genre, Movie, MovieRank, People, Comment, Score, MovieDip
from .crawling import movie_data

# Create your views here.
def list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/list.html', {'movies':movies})

@login_required
def detail(request, movie_id):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_id)
        comment_form = CommentForm()
        score_form = ScoreForm()
    return render(request, 'movies/detail.html', {'movie':movie, 'comment_form':comment_form, 'score_form':score_form})

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
    comment.delete()
    return redirect('movies:detail', movie_id)

def score_create(request, movie_id, score_id):
    pass

def score_update(request, movie_id, score_id):
    pass

def score_delete(request, movie_id, score_id):
    pass

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