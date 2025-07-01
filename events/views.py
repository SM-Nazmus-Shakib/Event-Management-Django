from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from datetime import date
from .models import Event, Participant, Category
from .forms import EventForm

def home(request):
    return render(request, 'events/home.html')

def dashboard(request):
    filter_type = request.GET.get('filter', 'all')
    events = Event.objects.all()
    
    if filter_type == 'upcoming':
        events = events.filter(date__gte=date.today())
    elif filter_type == 'past':
        events = events.filter(date__lt=date.today())

    todays_events = Event.objects.filter(date=date.today())
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=date.today()).count()
    past_events = Event.objects.filter(date__lt=date.today()).count()
    total_participants = Participant.objects.count()
    
    context = {
        'events': events,
        'todays_events': todays_events,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'total_participants': total_participants,
        'current_filter': filter_type,
    }
    return render(request, 'events/dashboard.html', context)

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('dashboard')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('dashboard')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'event': event})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('dashboard')
    return render(request, 'events/dashboard.html')