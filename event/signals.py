from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Location, Event


@receiver(pre_delete, sender=Location)
def reset_gmaps_tries(sender, instance, **kwargs):
    event = instance.event_set.first()
    event.gmaps_tries = 0
    event.save()
