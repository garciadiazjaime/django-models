from django.contrib import admin

from .models import Location, Event, GMapsLocation, Artist


class GMapsLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "lat", "lng"]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "gmaps_tries", "gmaps", "created", "updated"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "location", "gmaps", "created", "updated"]

    def name(self, obj):
        return obj.artist.name

    def gmaps(self, obj):
        return obj.location.gmaps


class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "wiki_page_id",
        "wiki_tries",
        "location",
        "created",
        "updated",
    ]

    def location(self, obj):
        return obj.event_set.first().location


admin.site.register(GMapsLocation, GMapsLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Artist, ArtistAdmin)

from django.contrib import admin
