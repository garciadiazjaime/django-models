from django.db import models


class GMapsLocation(models.Model):
    lat = models.DecimalField(max_digits=17, decimal_places=14, null=True, blank=True)
    lng = models.DecimalField(max_digits=17, decimal_places=14, null=True, blank=True)
    formatted_address = models.TextField()
    name = models.CharField(max_length=240)
    place_id = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lat}, {self.lng}"


class Location(models.Model):
    name = models.CharField(max_length=240)
    address = models.CharField(max_length=240, null=True, blank=True)
    city = models.CharField(max_length=240)
    state = models.CharField(max_length=240)

    gmaps_tries = models.PositiveSmallIntegerField(default=0)
    gmaps = models.ForeignKey(
        GMapsLocation, on_delete=models.CASCADE, null=True, blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=240)
    image = models.URLField(null=True, blank=True)
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
    description = models.CharField(null=True, blank=True, max_length=240)
    type = models.CharField(null=True, blank=True, max_length=240)
    wiki_page_id = models.CharField(null=True, blank=True, max_length=20)
    wiki_title = models.CharField(null=True, blank=True, max_length=240)
    wiki_description = models.CharField(null=True, blank=True, max_length=240)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    description = models.TextField(null=True, blank=True)
    image = models.URLField()
    url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist.name
