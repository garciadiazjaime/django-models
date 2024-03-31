import requests
import time
import environ
import random


from django.core.management.base import BaseCommand

from event.models import Artist, Twitter

env = environ.Env()


def get_twitter(handler):
    print(f"handler: {handler}")
    url = f"https://twitter.com/i/api/graphql/k5XapwcSikNsEsILW5FvgA/UserByScreenName?variables=%7B%22screen_name%22%3A%22{handler}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Atrue%2C%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D"

    headers = {
        "authorization": env("TWITTER_AUTHORIZATION"),
        "x-guest-token": env("TWITTER_GUEST_TOKEN"),
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"error:twitter response {response.status_code}")
        print(response.text)
        return -1

    data = response.json()

    if not "user" in data["data"]:
        print("error:user does not exist")
        return

    result = data["data"]["user"]["result"]

    if not "legacy" in result:
        print(f"error: {result['message']}")
        return

    image = (
        result["legacy"]["profile_banner_url"]
        if "profile_banner_url" in result["legacy"]
        else result["legacy"]["profile_image_url_https"]
    )

    # todo: some accounts have links to other sites, ie. fb, website
    twitter = {
        "handler": handler,
        "followers_count": result["legacy"]["followers_count"],
        "friends_count": result["legacy"]["friends_count"],
        "image": image,
    }

    return twitter


class Command(BaseCommand):
    def handle(self, **options):
        query = Artist.objects.filter(
            metadata__twitter__isnull=False, twitter__isnull=True
        ).exclude(metadata__twitter__exact="")

        print(f"total accounts: {query.count()}")

        list1 = [1, 2, 3, 5, 8, 13, 21]

        for artist in query:
            twitter_url = artist.metadata.twitter

            handler = twitter_url.split("/")[-1]
            twitter = get_twitter(handler.lower())

            if not twitter:
                print(f"removing metadata.twitter: {artist}[${artist.id}]")
                artist.metadata.twitter = ""
                artist.metadata.save()

            if twitter == -1:
                print(f"skipping: {handler}")
                continue

            Twitter.objects.update_or_create(artist=artist, defaults=twitter)

            wait = random.choice(list1)
            print(f"sleeping: for {wait} secs")
            time.sleep(wait)
