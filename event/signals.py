from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Location, Metadata, Artist


@receiver(pre_delete, sender=Location)
def reset_gmaps_tries(sender, instance, **kwargs):
    event = instance.event_set.first()
    event.gmaps_tries = 0
    event.save()


@receiver(pre_delete, sender=Metadata)
def reset_gmaps_tries(sender, instance, **kwargs):
    location = instance.location_set.first()
    if location:
        location.meta_tries = 0
        location.save()


@receiver(pre_delete, sender=Artist)
def reset_gmaps_tries(sender, instance, **kwargs):
    event = instance.event_set.first()

    if event.artists.count() == 1:
        event.artist_tries = 0
        event.save()
