from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True
    )
    profile_image = models.ImageField(
        upload_to='profile_images', 
        blank=True, 
        default='profile_images/default.png'
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username