from django.db import models
from autoslug import AutoSlugField


class Metadata(models.Model):
    wiki_page_id = models.PositiveIntegerField()
    wiki_title = models.CharField(null=True, blank=True, max_length=240)
    wiki_description = models.CharField(null=True, blank=True, max_length=120)
    website = models.URLField(null=True, blank=True)

    image = models.URLField(null=True, blank=True, max_length=240)
    twitter = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    tiktok = models.URLField(null=True, blank=True)
    soundcloud = models.URLField(null=True, blank=True)
    spotify = models.URLField(null=True, blank=True)
    appleMusic = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    title = models.CharField(null=True, blank=True, max_length=240)
    description = models.CharField(null=True, blank=True, max_length=960)
    type = models.CharField(null=True, blank=True, max_length=240)

    location_artist_slug = models.SlugField(max_length=240)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wiki_page_id}"


class Location(models.Model):
    name = models.CharField(max_length=240)
    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    place_id = models.CharField(max_length=50)

    wiki_tries = models.PositiveSmallIntegerField(default=0)
    metadata = models.ForeignKey(
        Metadata, on_delete=models.CASCADE, null=True, blank=True
    )

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    slug_venue = models.SlugField(max_length=240)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=240)

    wiki_tries = models.PositiveSmallIntegerField(default=0)
    metadata = models.ForeignKey(
        Metadata, on_delete=models.CASCADE, null=True, blank=True
    )

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
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

    slug = AutoSlugField(populate_from="name", editable=True, always_update=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
