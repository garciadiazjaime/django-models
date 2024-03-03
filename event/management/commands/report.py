from django.core.management.base import BaseCommand
from django.db.models import Count
from event.models import Location, Event

import csv


class Command(BaseCommand):
    def handle(self, **options):
        query = Location.objects.annotate(events=Count("event"))

        with open("location.csv", "w", newline="") as csv_file:
            file = csv.writer(
                csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            file.writerow(["id", "slug", "provider", "rank", "events", "lat", "lng"])
            for row in query:
                file.writerow(
                    [
                        row.id,
                        row.slug,
                        1 if row.provider == True else 0,
                        row.rank,
                        row.events,
                        row.lat,
                        row.lng,
                    ]
                )

        query = Event.objects.annotate(artists_count=Count("artists"))
        with open("events.csv", "w", newline="") as csv_file:
            file = csv.writer(
                csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            file.writerow(
                [
                    "id",
                    "slug",
                    "start_date",
                    "provider",
                    "price",
                    "buyUrl",
                    "venue",
                    "rank",
                    "artists",
                ]
            )
            for row in query:
                if row.location:
                    file.writerow(
                        [
                            row.id,
                            row.slug,
                            row.start_date,
                            row.provider,
                            row.price,
                            row.buyUrl,
                            row.location.slug,
                            row.rank,
                            row.artists_count,
                        ]
                    )
                else:
                    print("no location", row)
