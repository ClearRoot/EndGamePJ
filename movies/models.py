from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Genre(models.Model):
    mtype = models.CharField(max_length=30)
    
class Movie(models.Model):
    genre = models.ManyToManyField(Genre, related_name='movies', blank=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    open_date = models.CharField(max_length=10)
    audience = models.IntegerField(null=True)
    image = models.TextField()
    grade = models.CharField(max_length=30)
    nations = models.CharField(max_length=30)
    show_time = models.IntegerField()
    
class People(models.Model):
    movie = models.ManyToManyField(Movie, related_name='peoples', blank=True)
    director = models.CharField(max_length=50, blank=True)
    actor = models.CharField(max_length=150, blank=True)
    
class MovieRank(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.CharField(max_length=8)
    rank = models.IntegerField()
    rank_inten = models.IntegerField()
    
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
class Score(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(
        validators = (
            MaxValueValidator(5),
            MinValueValidator(0),
        )
    )
    create_at = models.DateTimeField(auto_now_add=True)