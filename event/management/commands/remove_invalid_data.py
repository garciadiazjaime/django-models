from django.db.models import Count
from django.core.management.base import BaseCommand
from event.models import Event, Metadata, GenerativeMetadata


def remove_duplicate_generative_metadata():
    duplicate_entries = (
        GenerativeMetadata.objects.values("event")
        .annotate(entry_count=Count("event"))
        .filter(entry_count__gt=1)
    )
    print(f"\nTotal generative metadata duplicate entries: {len(duplicate_entries)}")

    for entry in duplicate_entries:
        items = GenerativeMetadata.objects.filter(event=entry["event"])

        for item in items[1:]:
            item.delete()

    print("Done removing generative metadata duplicate entries")


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
                event.delete()

        print("Done removing duplicate entries")

        invalid_urls = [
            "http://www.facebook.com/pages",
            "https://www.facebook.com/pages",
            "https://www.facebook.com/profile",
            "http://www.facebook.com/profile",
            "https://www.facebook.com/tr",
            "http://www.facebook.com/tr",
            "http://www.facebook.com/2008",
            "https://www.facebook.com/share.php",
            "http://www.facebook.com/share.php",
        ]
        items = Metadata.objects.filter(facebook__in=invalid_urls)
        print(f"\nTotal invalid Facebook URLs: {len(items)}")
        for item in items:
            item.facebook = ""
            item.save()
        print("Done removing invalid Facebook URLs")

        remove_duplicate_generative_metadata()
