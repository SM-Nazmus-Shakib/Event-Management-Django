from django.urls import path
from events.views import dashboard, event_create, event_update, event_delete, rsvp_event

app_name = 'events'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', event_create, name='event-create'),
    path('<int:pk>/update/', event_update, name='event-update'),
    path('<int:pk>/delete/', event_delete, name='event-delete'),
    path('<int:pk>/rsvp/', rsvp_event, name='rsvp-event'),
]