from django.contrib import admin
from .models import Genre, Movie, People, Comment, Score, MovieVideo, RecommendMovie, SimilarMovie
# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(People)
admin.site.register(Comment)
admin.site.register(Score)
admin.site.register(MovieVideo)
admin.site.register(RecommendMovie)
admin.site.register(SimilarMovie)