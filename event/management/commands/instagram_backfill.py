import requests
import time
import environ
import random
import locale
from scrapy.selector import Selector
import json


from django.core.management.base import BaseCommand

from event.models import Artist, Instagram

env = environ.Env()
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


def parse_stat(formatted_stat):
    if not len(formatted_stat):
        return

    if formatted_stat[-1] == "M":
        return locale.atoi(formatted_stat[:-1]) * 1_000_000

    if formatted_stat[-1] == "K":
        return locale.atoi(formatted_stat[:-1]) * 1_000

    return locale.atoi(formatted_stat)


def get_instagram(url):
    response = requests.get(url)
    print(f"[{response.status_code}]: {url}")

    if response.status_code != 200:
        print(f"response: {response.status_code}")
        print(f"error: {response.text}")
        return -1

    description = Selector(text=response.text).xpath(
        "//meta[@name='description']/@content"
    )

    if not len(description):
        print("error:user does not exist")
        return -1

    meta_description_content = description[0].extract()
    stats_meta = meta_description_content.split("-")[0]

    stats_parts = stats_meta.split(" ")

    followers = parse_stat(stats_parts[0])
    following = parse_stat(stats_parts[2])
    posts = parse_stat(stats_parts[4])

    handle = url.split("/")[-2] if url[-1] == "/" else url.split("/")[-1]

    instagram = {
        "followers_count": followers,
        "following_count": following,
        "posts_count": posts,
        "handler": handle,
    }

    return instagram


class Command(BaseCommand):
    def handle(self, **options):
        query = Artist.objects.filter(
            metadata__instagram__isnull=False, instagram__isnull=True
        ).exclude(metadata__instagram__exact="")

        total = query.count()
        print(f"total accounts: {total}")

        wait_times = [5, 8, 13, 21, 34, 55]
        index = 1
        accounts_with_errors = []

        for artist in query:
            instagram_url = artist.metadata.instagram
            instagram = get_instagram(instagram_url)

            if instagram == -1:
                accounts_with_errors.append(instagram_url)

                if len(accounts_with_errors) > 6:
                    print(json.dumps(accounts_with_errors, indent=2))
                    print(f"early exit")
                    break

                print(f"skipping account: {instagram_url}")
                continue

            instance, _ = Instagram.objects.update_or_create(
                artist=artist, defaults=instagram
            )

            print(f"[{index}/{total}]: updated:{instance} ")

            wait = random.choice(wait_times)
            print(f"sleeping: for {wait} secs")
            time.sleep(wait)
            index += 1
