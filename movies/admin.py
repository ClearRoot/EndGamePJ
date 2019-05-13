from django.contrib import admin
from .models import Genre, Movie, People, MovieRank, Comment, Score, MovieDip
# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(People)
admin.site.register(MovieRank)
admin.site.register(Comment)
admin.site.register(Score)
admin.site.register(MovieDip)