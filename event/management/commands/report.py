import datetime
from pathlib import Path
import csv
import json
import boto3

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db.models import Count

from event.models import Location, Event, Artist
from event.support import loggerInfo

s3 = boto3.resource("s3")


def make_json(csv_file_path, json_file_path):
    file_content = {"created": str(datetime.date.today()), "data": []}

    with open(csv_file_path, encoding="utf-8") as csv_file:
        csvReader = csv.DictReader(csv_file)

        for rows in csvReader:
            file_content["data"].append(rows)

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(file_content, indent=4))


def export_locations():
    loggerInfo("exporting locations...")

    query = Location.objects.annotate(events=Count("event"))

    csv_file_name = "data/locations.csv"
    with open(csv_file_name, "w", newline="") as csv_file:
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

    json_file_name = "data/locations.json"
    make_json(csv_file_name, json_file_name)

    s3.meta.client.upload_file(
        Filename=csv_file_name,
        Bucket="cmc.data",
        Key=csv_file_name,
        ExtraArgs={
            "ContentType": "text/csv",
        },
    )

    s3.meta.client.upload_file(
        Filename=json_file_name,
        Bucket="cmc.data",
        Key=json_file_name,
        ExtraArgs={
            "ContentType": "application/json",
        },
    )

    loggerInfo("locations exported")


def export_events():
    loggerInfo("exporting events...")

    query = Event.objects.annotate(artists_count=Count("artists"))

    file_name = "data/events.csv"
    with open(file_name, "w", newline="") as csv_file:
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
                "created",
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
                        row.created.strftime("%Y-%m-%d"),
                    ]
                )
            else:
                loggerInfo("no location", row)

    json_file_name = "data/events.json"
    make_json(file_name, json_file_name)

    s3.meta.client.upload_file(
        Filename=file_name,
        Bucket="cmc.data",
        Key=file_name,
        ExtraArgs={
            "ContentType": "text/csv",
        },
    )

    s3.meta.client.upload_file(
        Filename=json_file_name,
        Bucket="cmc.data",
        Key=json_file_name,
        ExtraArgs={
            "ContentType": "application/json",
        },
    )

    loggerInfo("events exported")


def get_group(followers):
    if not followers or followers < 10_000:
        return 1

    if followers < 1_000_000:
        return 2

    return 3


def get_popularity(popularity):
    if not popularity or popularity < 40:
        return 1

    if popularity < 80:
        return 2

    return 3


def export_artist():
    loggerInfo("exporting artists...")

    query = Artist.objects.filter(musico__isnull=False).annotate(
        events_count=Count("event")
    )

    file_name = "data/artists.csv"
    with open(file_name, "w", newline="") as csv_file:
        file = csv.writer(
            csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        file.writerow(
            [
                # "genres_count",
                "spotify",
                "website",
                "twitter",
                "facebook",
                "youtube",
                "instagram",
                "tiktok",
                "soundcloud",
                "appleMusic",
                # "band_camp",
                # "link_tree",
                # "group",
                "popularity",
            ]
        )

        for row in query:
            group = get_group(row.musico_set.first().followers)
            popularity = get_popularity(row.musico_set.first().popularity)
            file.writerow(
                [
                    # row.genres.count(),
                    1 if row.spotify else 0,
                    1 if hasattr(row.metadata, "website") else 0,
                    1 if hasattr(row.metadata, "twitter") else 0,
                    1 if hasattr(row.metadata, "facebook") else 0,
                    1 if hasattr(row.metadata, "youtube") else 0,
                    1 if hasattr(row.metadata, "instagram") else 0,
                    1 if hasattr(row.metadata, "tiktok") else 0,
                    1 if hasattr(row.metadata, "soundcloud") else 0,
                    1 if hasattr(row.metadata, "appleMusic") else 0,
                    # 1 if hasattr(row.metadata, "band_camp") else 0,
                    # 1 if hasattr(row.metadata, "link_tree") else 0,
                    # group,
                    popularity,
                ]
            )

    json_file_name = "data/artists.json"
    with open(file_name, newline="") as csv_file:
        make_json(file_name, json_file_name)
        default_storage.save(file_name, csv_file)

    with open(json_file_name, newline="") as json_file:
        default_storage.save(json_file_name, json_file)

    loggerInfo("artists exported")


def export_artist_twitter():
    loggerInfo("exporting artists with twitter...")

    query = (
        Artist.objects.filter(musico__isnull=False, twitter__followers_count__gt=0)
        .annotate(events_count=Count("event"))
        .order_by("-twitter__followers_count")
    )
    loggerInfo(f"artists found: {query.count()}")

    file_name = "data/artists.csv"
    with open(file_name, "w", newline="") as csv_file:
        file = csv.writer(
            csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        file.writerow(
            [
                # "spotify",
                # "spotify_followers",
                # "website",
                # "twitter",
                "twitter_followers",
                # "facebook",
                # "youtube",
                # "instagram",
                # "tiktok",
                # "soundcloud",
                # "appleMusic",
                "popularity",
                "handle",
            ]
        )

        for artist in query:
            # popularity = get_popularity(artist.musico_set.first().popularity)
            file.writerow(
                [
                    # 1 if artist.spotify else 0,
                    # artist.spotify.followers if artist.spotify else 0,
                    # 1 if hasattr(artist.metadata, "website") else 0,
                    # 1 if hasattr(artist.metadata, "twitter") else 0,
                    artist.twitter_set.first().followers_count,
                    # 1 if hasattr(artist.metadata, "facebook") else 0,
                    # 1 if hasattr(artist.metadata, "youtube") else 0,
                    # 1 if hasattr(artist.metadata, "instagram") else 0,
                    # 1 if hasattr(artist.metadata, "tiktok") else 0,
                    # 1 if hasattr(artist.metadata, "soundcloud") else 0,
                    # 1 if hasattr(artist.metadata, "appleMusic") else 0,
                    artist.musico_set.first().popularity,
                    artist.twitter_set.first().handler,
                ]
            )

    # json_file_name = "data/artists.json"

    # make_json(file_name, json_file_name)
    # s3.meta.client.upload_file(
    #     Filename=file_name,
    #     Bucket="cmc.data",
    #     Key=file_name,
    #     ExtraArgs={
    #         "ContentType": "text/csv",
    #     },
    # )

    # s3.meta.client.upload_file(
    #     Filename=json_file_name,
    #     Bucket="cmc.data",
    #     Key=json_file_name,
    #     ExtraArgs={
    #         "ContentType": "application/json",
    #     },
    # )

    loggerInfo("artists exported")


class Command(BaseCommand):
    def handle(self, **options):
        Path("./data").mkdir(parents=True, exist_ok=True)

        loggerInfo(f"exporting data {str(datetime.date.today())}")

        # export_locations()
        # export_events()
        # export_artist()
        export_artist_twitter()

        loggerInfo("export completed")
