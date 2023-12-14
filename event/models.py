from django.db import models
from autoslug import AutoSlugField

METADATA_CHOICES = [("ARTIST", "ARTIST"), ("LOCATION", "LOCATION")]


class Metadata(models.Model):
    slug = models.SlugField(max_length=240)
    type = models.CharField(max_length=24, choices=METADATA_CHOICES)
    website = models.URLField(default="", blank=True)
    image = models.URLField(default="", blank=True, max_length=240)
    twitter = models.URLField(default="", blank=True)
    facebook = models.URLField(default="", blank=True)
    youtube = models.URLField(default="", blank=True)
    instagram = models.URLField(default="", blank=True)
    tiktok = models.URLField(default="", blank=True)
    soundcloud = models.URLField(default="", blank=True)
    spotify = models.URLField(default="", blank=True)
    appleMusic = models.URLField(default="", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug


class Artist(models.Model):
    name = models.CharField(max_length=240)
    profile = models.URLField()

    metadata = models.ForeignKey(
        Metadata, on_delete=models.SET_NULL, null=True, blank=True
    )

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=240)
    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    place_id = models.CharField(max_length=50)
    website = models.URLField(default="")

    meta_tries = models.PositiveSmallIntegerField(default=0)
    metadata = models.ForeignKey(
        Metadata, on_delete=models.SET_NULL, null=True, blank=True
    )

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    slug_venue = models.SlugField(max_length=240)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=240)
    description = models.TextField(default="", blank=True)
    image = models.URLField()
    url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    provider = models.CharField(max_length=240)

    venue = models.CharField(max_length=240)
    address = models.CharField(max_length=240, default="", blank=True)
    city = models.CharField(max_length=240)

    rank = models.PositiveSmallIntegerField(default=0)

    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    gmaps_tries = models.PositiveSmallIntegerField(default=0)

    artists = models.ManyToManyField(Artist, blank=True)
    artist_tries = models.PositiveSmallIntegerField(default=0)

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
