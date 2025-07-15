from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from datetime import date
from events.models import Event,Category,Participant
from events.forms import EventModelForm

User = get_user_model()

@login_required
def dashboard(request):
    filter_type = request.GET.get('filter', 'all')
    events = Event.objects.all()
    
    if not request.user.has_perm('events.can_manage_events'):
        events = events.filter(participants__user=request.user) | events.filter(created_by=request.user)
    
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
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventModelForm(request.POST, request=request)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()
            messages.success(request, 'Event created successfully!')
            return redirect('events:dashboard')
    else:
        form = EventModelForm(request=request)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.has_perm('events.can_manage_events') and event.created_by != request.user:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('events:dashboard')
        
    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=event, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:dashboard')
    else:
        form = EventModelForm(instance=event, request=request)
    return render(request, 'events/event_form.html', {'form': form, 'event': event})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.has_perm('events.can_manage_events') and event.created_by != request.user:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('events:dashboard')
        
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('events:dashboard')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def rsvp_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participant, created = Participant.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.get_full_name(), 'email': request.user.email}
    )
    
    if request.method == 'POST':
        if event.participants.filter(pk=participant.pk).exists():
            event.participants.remove(participant)
            messages.success(request, 'You have canceled your RSVP.')
        else:
            event.participants.add(participant)
            messages.success(request, 'Successfully RSVPed to the event!')
    return redirect('events:dashboard')