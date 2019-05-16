from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    mtype = models.CharField(max_length=30)
    
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    genre = models.ManyToManyField(Genre, related_name='movies', blank=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.TextField()
    back_image = models.TextField()
    open_date = models.CharField(max_length=4, blank=True)
    def __str__(self):
        return self.title
    
class People(models.Model):
    movie = models.ManyToManyField(Movie, related_name='peoples', blank=True)
    people_key = models.IntegerField()
    actor = models.CharField(max_length=150, blank=True)
    director = models.CharField(max_length=50, blank=True)
    image = models.TextField(null=True)
    
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
    
class MovieVideo(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True)
    key = models.TextField()
    name = models.TextField()
    site = models.TextField()
    size = models.TextField()
    vtype = models.TextField()
    
class RecommendMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    code = models.IntegerField()
    
class SimilarMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    code = models.IntegerField()