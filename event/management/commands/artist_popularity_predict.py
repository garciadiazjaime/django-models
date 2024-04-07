import tensorflow as tf
from django.core.management.base import BaseCommand
import numpy as np
import math

from event.models import Artist


class Command(BaseCommand):
    def handle(self, **options):

        reloaded = tf.keras.models.load_model("./data/artist_popularity_model.keras")

        artists = Artist.objects.filter(
            twitter__isnull=False,
        )

        for artist in artists:
            followers_count = max(artist.twitter_set.first().followers_count, 1)
            followers_count = math.log(followers_count)
            x = np.array([followers_count])
            y = reloaded.predict(x) * 100

            artist.popularity = y
            artist.save()
