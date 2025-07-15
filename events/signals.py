from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Event, Participant
from django.template.loader import render_to_string

@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        participants = Participant.objects.filter(pk__in=pk_set)
        for participant in participants:
            if participant.email:
                subject = f"Invitation to {instance.name}"
                message = render_to_string('events/email/invitation.txt', {
                    'event': instance,
                    'participant': participant,
                })
                send_mail(
                    subject,
                    message,
                    'noreply@yourevents.com',
                    [participant.email],
                    fail_silently=True,
                )

@receiver(post_delete, sender=Event)
def log_event_deletion(sender, instance, **kwargs):
    # In production, you might want to use logging instead of print
    print(f"Event '{instance.name}' was deleted")

@receiver(post_save, sender=Event)
def set_event_creator(sender, instance, created, **kwargs):
    if created and not instance.created_by:
        # This ensures created_by is set when event is created through admin or other means
        if hasattr(instance, 'creator'):
            instance.created_by = instance.creator
            instance.save()