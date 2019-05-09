from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Genre(models.Model):
    mtype = models.CharField(max_length=30)
    def __str__(self):
        return self.mtype
    
class Movie(models.Model):
    genres = models.ManyToManyField(Genre, related_name='movies')
    title = models.CharField(max_length=150)
    content = models.TextField()
    open_date = models.CharField(max_length=8)
    audience = models.IntegerField()
    image = ProcessedImageField(
            upload_to = 'movies/images',
            processors = [ResizeToFill(400,600)],
            format = 'JPEG',
            options = {'quality':100},
        )
    grade = models.CharField(max_length=30)
    nations = models.CharField(max_length=30)
    show_time = models.CharField(max_length=3)
    
class People(models.Model):
    movies = models.ManyToManyField(Movie, related_name='peoples')
    director = models.CharField(max_length=50, blank=True)
    actor = models.CharField(max_length=150, blank=True)
    
class MovieRank(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.CharField(max_length=8)
    rank = models.IntegerField()
    rank_inten = models.IntegerField()