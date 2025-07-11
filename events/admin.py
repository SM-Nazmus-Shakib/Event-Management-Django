from django.contrib import admin
from .models import Event, Category

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'created_by', 'participants_count')
    list_filter = ('date', 'category', 'created_by')
    search_fields = ('name', 'description')
    filter_horizontal = ('participants',)
    
    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = 'Participants'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_count')
    search_fields = ('name',)
    
    def event_count(self, obj):
        return obj.event_set.count()
    event_count.short_description = 'Events'