from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        # Generate activation token and URL
        from django.contrib.auth.tokens import default_token_generator
        token = default_token_generator.make_token(instance)
        activation_url = reverse('users:activate-user', kwargs={
            'user_id': instance.id,
            'token': token
        })
        full_url = f"{settings.SITE_URL}{activation_url}"
        
        # Email content
        subject = 'Activate Your Account'
        message = f"""Hello {instance.username},

Please click the following link to activate your account:
{full_url}

If you didn't request this, please ignore this email.

Best regards,
EventPro Team
"""
        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )

        # Assign default group if exists
        from django.contrib.auth.models import Group
        try:
            user_group = Group.objects.get(name='User')
            instance.groups.add(user_group)
        except Group.DoesNotExist:
            pass