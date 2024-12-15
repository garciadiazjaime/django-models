from django.db.models import Count
from django.core.management.base import BaseCommand
from event.models import Event


class Command(BaseCommand):
    def handle(self, **options):
        duplicate_entries = (
            Event.objects.values("url", "location", "start_date")
            .annotate(entry_count=Count("id"))
            .filter(entry_count__gt=1)
        )
        print(f"Total duplicate entries: {len(duplicate_entries)}")

        for entry in duplicate_entries:
            events = Event.objects.filter(
                url=entry["url"], location=entry["location"]
            ).order_by("-created")

            for event in events[1:]:
                print(".", end="", flush=True)
                event.delete()

        print("\nDone")
