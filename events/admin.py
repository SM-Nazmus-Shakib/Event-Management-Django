from django.contrib import admin
from .models import Event, Category,Participant

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Participant)