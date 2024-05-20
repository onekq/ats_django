import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import AuditLog, JobRequirement, JobApplication, Applicant

logger = logging.getLogger(__name__)

@receiver(post_save, sender=JobRequirement)
@receiver(post_save, sender=JobApplication)
@receiver(post_save, sender=Applicant)
def log_create_update(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    try:
        AuditLog.objects.create(
            resource_name=sender.__name__,
            action=action,
            payload=model_to_dict(instance)
        )
    except Exception as e:
        logger.error(f'Error logging {action} for {sender.__name__}: {e}')

@receiver(pre_delete, sender=JobRequirement)
@receiver(pre_delete, sender=JobApplication)
@receiver(pre_delete, sender=Applicant)
def log_delete(sender, instance, **kwargs):
    try:
        AuditLog.objects.create(
            resource_name=sender.__name__,
            action='DELETE',
            payload=model_to_dict(instance)
        )
    except Exception as e:
        logger.error(f'Error logging DELETE for {sender.__name__}: {e}')
