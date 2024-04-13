import requests
import time
import environ
import random
import re
import locale
from scrapy.selector import Selector

from django.core.management.base import BaseCommand

from event.models import Artist, Instagram

env = environ.Env()
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def parse_stat(formatted_stat):
    if not len(formatted_stat):
        return None

    if formatted_stat[-1] == "M":
        return locale.atoi(formatted_stat[:-1]) * 1_000_000

    if formatted_stat[-1] == "K":
        return locale.atoi(formatted_stat[:-1]) * 1_000

    return locale.atoi(formatted_stat)
    

def get_instagram(url):
    print(f"url: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"response: {response.status_code}")
        print(f"error: {response.text}")
        return -1

    meta_description_content = Selector(text=response.text).xpath("//meta[@name='description']/@content")[0].extract()
    stats_meta, handler_meta = meta_description_content.split("-")

    stats_parts = stats_meta.split()
    
    followers=parse_stat(stats_parts[0])  
    following=parse_stat(stats_parts[2])
    posts=parse_stat(stats_parts[4])

    handler_matches = re.findall(r"\((.*?)\)", handler_meta)
    handler = handler_matches[0] if len(handler_matches) else ""

    instagram = {
        "followers_count": followers,
        "following_count": following,
        "posts_count": posts,
        "handler": handler
    }

    return instagram


class Command(BaseCommand):
    def handle(self, **options):
        query = Artist.objects.filter(
            metadata__instagram__isnull=False, instagram__isnull=True
        ).exclude(metadata__instagram__exact="")

        print(f"total accounts: {query.count()}")

        wait_times = [8, 13, 21, 34, 55]

        for artist in query:
            instagram_url = artist.metadata.instagram
            instagram = get_instagram(instagram_url)
            
            if not instagram:
                print(f"removing metadata.instagram: {artist}[${artist.id}]")
                artist.metadata.instagram = ""
                artist.metadata.save()

            if instagram == -1:
                print(f"early exit")
                break

            instance,_ = Instagram.objects.update_or_create(artist=artist, defaults=instagram)
            
            print(f"updated:{instance}")
            wait = random.choice(wait_times)
            print(f"sleeping: for {wait} secs")
            time.sleep(wait)
