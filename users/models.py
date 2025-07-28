from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from event_management import settings

class User(AbstractUser):
    # Phone number field with better validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in international format: '+999999999'."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        unique=True  # Added unique constraint
    )
    
    # Profile picture with validation
    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ],
        help_text="Maximum 2MB. JPG or PNG only."
    )
    
    # Bio with character limit
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=1000,
        help_text="Tell us about yourself (1000 characters max)"
    )

    def clean(self):
        # Add model-level validation
        if self.phone_number:
            self.phone_number = self.phone_number.strip()
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation before save
        super().save(*args, **kwargs)

    def get_profile_picture_url(self):
        """Safe method to get profile picture URL"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return settings.MEDIA_URL + 'event/default_img.png'