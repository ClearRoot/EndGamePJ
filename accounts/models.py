from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)
    introduce = models.CharField(max_length=50)
    profile_image= ProcessedImageField(
        upload_to= 'accounts/images',
        processors= [ResizeToFill(150,150)],
        format= 'JPEG',
        options= {'quality':90},
        blank=True
    )
    pass