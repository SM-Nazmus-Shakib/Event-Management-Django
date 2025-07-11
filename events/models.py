from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import os

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='events_participating')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created',default=1 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
    upload_to='event/',
    default='default_img.jpg')
    class Meta:
        ordering = ['-date']
        permissions = [
            ("can_manage_events", "Can create, update, and delete events"),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.date})"
