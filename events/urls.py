from django.urls import path
from events.views import dashboard,event_create,event_update,event_delete,rsvp_event

urlpatterns = [
    path('events/dashboard', dashboard, name='dashboard'),
    path('events/create/', event_create, name='event-create'),
    path('events/<int:pk>/update/', event_update, name='event-update'),
    path('events/<int:pk>/delete/', event_delete, name='event-delete'),
    path('events/<int:pk>/rsvp/', rsvp_event, name='rsvp-event')
]