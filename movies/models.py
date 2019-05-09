from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Genre(models.Model):
    mtype = models.CharField(max_length=30)
    def __str__(self):
        return self.mtype
    
class Movie(models.Model):
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    open_date = models.CharField(max_length=10)
    audience = models.IntegerField(null=True)
    image = models.TextField()
    grade = models.CharField(max_length=30)
    nations = models.CharField(max_length=30)
    show_time = models.IntegerField()
    
class People(models.Model):
    movies = models.ManyToManyField(Movie, related_name='peoples', blank=True)
    director = models.CharField(max_length=50, blank=True)
    actor = models.CharField(max_length=150, blank=True)
    
class MovieRank(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.CharField(max_length=8)
    rank = models.IntegerField()
    rank_inten = models.IntegerField()