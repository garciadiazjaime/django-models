from django.contrib import admin

from .models import Location, Event, GMapsLocation, Artist, Metadata


class GMapsLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "lat", "lng", "created", "updated"]
    search_fields = ["name"]


class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "gmaps_tries",
        "gmaps",
        "wiki_tries",
        "metadata",
        "created",
        "updated",
    ]
    search_fields = ["name"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "location", "gmaps", "created", "updated"]
    search_fields = ["artist__name"]

    def name(self, obj):
        return obj.artist.name

    def gmaps(self, obj):
        return obj.location.gmaps


class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "wiki_page_id",
        "wiki_tries",
        "created",
        "updated",
    ]
    search_fields = ["name"]

    def wiki_page_id(self, obj):
        return obj.metadata


class MetadataAdmin(admin.ModelAdmin):
    list_display = [
        "wiki_page_id",
        "slug",
        "website",
        "created",
        "updated",
    ]
    search_fields = ["wiki_title"]


admin.site.register(GMapsLocation, GMapsLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Metadata, MetadataAdmin)

from django.contrib import admin
