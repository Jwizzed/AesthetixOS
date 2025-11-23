from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction
from tasks.commission_tasks import calculate_commission

@receiver(post_save, sender=Transaction)
def trigger_commission_calculation(sender, instance, created, **kwargs):
    """
    Trigger async commission calculation when a transaction is marked COMPLETED.
    """
    if instance.status == 'COMPLETED':
        # Use .delay() to offload to Celery
        # We pass the ID, not the object, to avoid serialization issues
        calculate_commission.delay(instance.id)

