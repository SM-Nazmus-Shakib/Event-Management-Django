from django.urls import path
from events.views import home,dashboard,event_create,event_update,event_delete

urlpatterns = [
    path('', home,name='home'),
    path('dashboard/',dashboard,name='dashboard'),
    path('events/create/',event_create,name='event-create'),
    path('events/<int:pk>/update/',event_update,name='event-update'),
    path('events/<int:pk>/delete/',event_delete, name='event-delete'),
]