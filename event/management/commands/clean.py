from django.core.management.base import BaseCommand
from django.db.models import Count

from event.models import Artist


class Command(BaseCommand):
    def handle(self, **options):
        duplicates = (
            Artist.objects.values("slug")
            .annotate(count=Count("slug"))
            .filter(count__gt=1)
        )

        print(len(duplicates), "duplicates found")
        for row in duplicates:
            artist = Artist.objects.filter(slug=row["slug"]).first()
            artist.delete()

        print("duplicates removed")
