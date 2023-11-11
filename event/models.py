from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=240)
    locality = models.CharField(max_length=240, blank=True)
    postal = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=240)
    state = models.CharField(max_length=240)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.locality} - {self.street}"


class Location(models.Model):
    name = models.CharField(max_length=240)
    url = models.URLField()
    telephone = models.CharField(max_length=20, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Organizer(models.Model):
    name = models.CharField(max_length=240)

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
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, null=True, blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
