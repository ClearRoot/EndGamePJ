from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    profile_image= ProcessedImageField(
        upload_to= 'accounts/images',
        processors= [ResizeToFill(150,150)],
        format= 'JPEG',
        options= {'quality':90},
        blank=True
    )
    pass