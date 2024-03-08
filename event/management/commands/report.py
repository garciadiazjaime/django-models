from django.core.management.base import BaseCommand
from django.db.models import Count
from event.models import Location, Event, Artist

import csv


def export_locations():
    print("exporting locations...")

    query = Location.objects.annotate(events=Count("event"))

    with open("./data/location.csv", "w", newline="") as csv_file:
        file = csv.writer(
            csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        file.writerow(
            [
                "id",
                "lat",
                "lng",
                "website",
                "provider",
                "rank",
                "slug",
                "events",
                "image",
                "twitter",
                "facebook",
                "youtube",
                "instagram",
                "tiktok",
                "soundcloud",
                "appleMusic",
                "spotify",
                "band_camp",
                "link_tree",
            ]
        )

        for row in query:
            file.writerow(
                [
                    row.id,
                    row.lat,
                    row.lng,
                    1 if row.website else 0,
                    1 if row.provider == True else 0,
                    row.rank,
                    row.slug,
                    row.events,
                    1 if hasattr(row.metadata, "image") and row.metadata.image else 0,
                    (
                        1
                        if hasattr(row.metadata, "twitter") and row.metadata.twitter
                        else 0
                    ),
                    (
                        1
                        if hasattr(row.metadata, "facebook") and row.metadata.facebook
                        else 0
                    ),
                    (
                        1
                        if hasattr(row.metadata, "youtube") and row.metadata.youtube
                        else 0
                    ),
                    (
                        1
                        if hasattr(row.metadata, "instagram") and row.metadata.instagram
                        else 0
                    ),
                    1 if hasattr(row.metadata, "tiktok") and row.metadata.tiktok else 0,
                    (
                        1
                        if hasattr(row.metadata, "soundcloud")
                        and row.metadata.soundcloud
                        else 0
                    ),
                    (
                        1
                        if hasattr(row.metadata, "appleMusic")
                        and row.metadata.appleMusic
                        else 0
                    ),
                    (
                        1
                        if hasattr(row.metadata, "spotify") and row.metadata.spotify
                        else 0
                    ),
                    (
                        1
                        if hasattr(row.metadata, "band_camp") and row.metadata.band_camp
                        else 0
                    ),
                    (
                        1
                        if hasattr(row.metadata, "link_tree") and row.metadata.link_tree
                        else 0
                    ),
                ]
            )

    print("locations exported")


def export_events():
    print("exporting events...")

    query = Event.objects.annotate(artists_count=Count("artists"))
    with open("./data/events.csv", "w", newline="") as csv_file:
        file = csv.writer(
            csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        file.writerow(
            [
                "id",
                "start_date",
                "provider",
                "price",
                "rank",
                "slug",
                "artists_count",
                "venue",
            ]
        )

        for row in query:
            if row.location:
                file.writerow(
                    [
                        row.id,
                        row.start_date,
                        row.provider,
                        row.price,
                        row.rank,
                        row.slug,
                        row.artists_count,
                        row.location.slug,
                    ]
                )
            else:
                print("no location", row)

    print("events exported")


def export_artist():
    print("exporting artists...")

    query = Artist.objects.annotate(events_count=Count("event"))
    with open("./data/artists.csv", "w", newline="") as csv_file:
        file = csv.writer(
            csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        file.writerow(
            [
                "id",
                "profile",
                "genres_count",
                "spotify",
                "slug",
                "image",
                "twitter",
                "facebook",
                "youtube",
                "instagram",
                "tiktok",
                "soundcloud",
                "appleMusic",
                "spotify",
                "band_camp",
                "link_tree",
            ]
        )

        for row in query:
            file.writerow(
                [
                    row.id,
                    row.profile,
                    row.genres.count(),
                    row.spotify,
                    row.slug,
                    (
                        row.metadata.facebook
                        if hasattr(row.metadata, "facebook")
                        else None
                    ),
                    row.metadata.youtube if hasattr(row.metadata, "youtube") else None,
                    (
                        row.metadata.instagram
                        if hasattr(row.metadata, "instagram")
                        else None
                    ),
                    row.metadata.tiktok if hasattr(row.metadata, "tiktok") else None,
                    (
                        row.metadata.soundcloud
                        if hasattr(row.metadata, "soundcloud")
                        else None
                    ),
                    (
                        row.metadata.appleMusic
                        if hasattr(row.metadata, "appleMusic")
                        else None
                    ),
                    row.metadata.spotify if hasattr(row.metadata, "spotify") else None,
                    (
                        row.metadata.band_camp
                        if hasattr(row.metadata, "band_camp")
                        else None
                    ),
                    (
                        row.metadata.link_tree
                        if hasattr(row.metadata, "link_tree")
                        else None
                    ),
                ]
            )

    print("artists exported")


class Command(BaseCommand):
    def handle(self, **options):
        export_locations()
        export_events()
        export_artist()
