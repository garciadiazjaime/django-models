from django.db import models
from autoslug import AutoSlugField

METADATA_CHOICES = [("ARTIST", "ARTIST"), ("LOCATION", "LOCATION")]


class Genre(models.Model):
    name = models.CharField(max_length=240)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Slug(models.Model):
    name = models.CharField(max_length=240)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Spotify(models.Model):
    name = models.CharField(max_length=240)
    followers = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, blank=True)
    popularity = models.IntegerField(default=0)
    url = models.URLField(default="", blank=True)
    image = models.URLField(default="", blank=True, max_length=240)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Metadata(models.Model):
    slug = models.SlugField(max_length=240)
    type = models.CharField(max_length=24, choices=METADATA_CHOICES)
    website = models.URLField(default="", blank=True)
    image = models.URLField(default="", blank=True, max_length=420)
    twitter = models.URLField(default="", blank=True)
    facebook = models.URLField(default="", blank=True)
    youtube = models.URLField(default="", blank=True)
    instagram = models.URLField(default="", blank=True)
    tiktok = models.URLField(default="", blank=True)
    soundcloud = models.URLField(default="", blank=True)
    appleMusic = models.URLField(default="", blank=True)
    spotify = models.URLField(default="", blank=True)
    band_camp = models.URLField(default="", blank=True)
    link_tree = models.URLField(default="", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website


class Artist(models.Model):
    name = models.CharField(max_length=240)
    profile = models.URLField(default="", null=True, blank=True)
    popularity = models.IntegerField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    spotify = models.ForeignKey(
        Spotify, on_delete=models.CASCADE, null=True, blank=True
    )

    metadata = models.ForeignKey(
        Metadata, on_delete=models.CASCADE, null=True, blank=True
    )

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MusicO(models.Model):
    followers = models.IntegerField(blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)
    image = models.URLField(default="", blank=True, null=True, max_length=420)
    genres = models.ManyToManyField(Genre, blank=True)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Location(models.Model):
    name = models.CharField(max_length=240)
    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    place_id = models.CharField(max_length=50)
    website = models.URLField(null=True, blank=True, default="")
    url = models.URLField(null=True, blank=True, default="")
    provider = models.BooleanField(default=False)

    metadata = models.ForeignKey(
        Metadata, on_delete=models.CASCADE, null=True, blank=True
    )

    rank = models.PositiveSmallIntegerField(default=0)

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    slug_venue = models.ManyToManyField(Slug, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=240)
    description = models.TextField(default="", blank=True)
    image = models.URLField()
    url = models.URLField(max_length=420)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    provider = models.CharField(max_length=240)
    price = models.FloatField(default=0, null=True, blank=True)
    buyUrl = models.URLField(default="", blank=True, max_length=420)

    venue = models.CharField(max_length=240)
    address = models.CharField(max_length=240, default="", blank=True)
    city = models.CharField(max_length=240)

    rank = models.PositiveSmallIntegerField(default=0)

    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    artists = models.ManyToManyField(Artist, blank=True)

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Twitter(models.Model):
    handler = models.CharField(max_length=240)
    followers_count = models.IntegerField(default=0)
    friends_count = models.IntegerField(default=0)
    image = models.URLField(default="", blank=True, max_length=240)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.handler


class Instagram(models.Model):
    handler = models.CharField(max_length=240)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.handler
