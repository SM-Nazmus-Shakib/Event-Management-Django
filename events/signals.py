from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Event
from django.contrib.auth.models import User

@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants(sender, instance, action, **kwargs):
    if action == 'post_add':
        participant_emails = [user.email for user in instance.participants.all()]
        
        send_mail(
            "New Event Invitation",
            f"You have been invited to the event: {instance.name} on {instance.date}",
            "noreply@yourevents.com",
            participant_emails,
            fail_silently=False,
        )

@receiver(post_delete, sender=Event)
def log_event_deletion(sender, instance, **kwargs):
    print(f"Event '{instance.name}' was deleted")

@receiver(post_save, sender=Event)
def add_creator_as_host(sender, instance, created, **kwargs):
    if created:
        try:
            if hasattr(instance.created_by, 'userprofile'):
                instance.created_by.userprofile.hosted_events.add(instance)
        except Exception as e:
            print(f"Could not add host: {e}")  # For debugging