from django.db import models


class Place(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=240)
    photo_reference = models.CharField(max_length=200, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    place_id = models.CharField(max_length=240)
    price_level = models.PositiveSmallIntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    types = models.CharField(max_length=240)
    user_ratings_total = models.PositiveSmallIntegerField(null=True, blank=True)
    vicinity = models.CharField(max_length=240, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    permanently_closed = models.BooleanField(default=False)
    gmaps_tries = models.PositiveSmallIntegerField(default=0)
