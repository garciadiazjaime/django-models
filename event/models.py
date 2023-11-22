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


class Event(models.Model):
    name = models.CharField(max_length=240)
    description = models.TextField()
    image = models.URLField()
    url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
