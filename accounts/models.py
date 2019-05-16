from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from movies.models import Movie

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)
    introduce = models.CharField(max_length=60, blank=True)
    pick_movie = models.ManyToManyField(Movie, related_name='pick_user', blank=True)
    profile_image= ProcessedImageField(
        upload_to= 'accounts/images',
        processors= [ResizeToFill(150,150)],
        format= 'JPEG',
        options= {'quality':90},
        blank=True
    )