from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from datetime import date
from .models import Event, Category
from .forms import EventModelForm

@login_required
def dashboard(request):
    filter_type = request.GET.get('filter', 'all')
    events = Event.objects.all()
    
    if not request.user.has_perm('events.can_manage_events'):
        events = events.filter(participants=request.user)
    
    if filter_type == 'upcoming':
        events = events.filter(date__gte=date.today())
    elif filter_type == 'past':
        events = events.filter(date__lt=date.today())

    todays_events = events.filter(date=date.today())
    total_events = events.count()
    upcoming_events = events.filter(date__gte=date.today()).count()
    past_events = events.filter(date__lt=date.today()).count()
    
    context = {
        'events': events,
        'todays_events': todays_events,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'current_filter': filter_type,
    }
    return render(request, 'events/dashboard.html', context)

@login_required
@permission_required('events.can_manage_events', raise_exception=True)
def event_create(request):
    if request.method == 'POST':
        form = EventModelForm(request.POST, request=request)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Event created successfully!')
            return redirect('dashboard')
    else:
        form = EventModelForm(request=request)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.has_perm('events.can_manage_events') and event.created_by != request.user:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=event, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('dashboard')
    else:
        form = EventModelForm(instance=event, request=request)
    return render(request, 'events/event_form.html', {'form': form, 'event': event})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.has_perm('events.can_manage_events') and event.created_by != request.user:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')
@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if event.participants.filter(id=request.user.id).exists():
            messages.warning(request, 'You have already RSVPed to this event.')
        else:
            event.participants.add(request.user)
            messages.success(request, 'Successfully RSVPed to the event!')
    return redirect('dashboard')
