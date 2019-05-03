from django.shortcuts import render, redirect

# Create your views here.
def list(request):
    return render(request, 'movies/list.html')