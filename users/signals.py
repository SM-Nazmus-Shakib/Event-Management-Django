from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        try:
            # Using request.build_absolute_uri for proper URL generation
            token = default_token_generator.make_token(instance)
            activation_url = reverse(
                'users:activate-user',
                kwargs={'user_id': instance.id, 'token': token}
            )
            
            # Get current site domain properly
            from django.contrib.sites.shortcuts import get_current_site
            current_site = get_current_site(None)
            full_url = f"https://{current_site.domain}{activation_url}"
            
            send_mail(
                'Activate Your EventPro Account',
                f"""Hello {instance.username},
                
Please click the link below to activate your account:
{full_url}

If you didn't request this, please ignore this email.

Thank you,
EventPro Team""",
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Activation email failed for {instance.email}: {str(e)}")
            # Consider adding admin notification here