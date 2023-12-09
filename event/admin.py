from django.contrib import admin

from .models import Location, Event, Artist, Metadata


class MetadataAdmin(admin.ModelAdmin):
    list_display = [
        "wiki_page_id",
        "location_artist_slug",
        "website",
        "created",
        "updated",
    ]
    search_fields = ["wiki_title"]


class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "lat", "lng", "created", "updated"]
    search_fields = ["name"]


class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "wiki_page_id",
        "wiki_tries",
        "created",
        "updated",
    ]
    search_fields = ["name"]

    def wiki_page_id(self, obj):
        return obj.metadata


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "slug",
        "venue",
        "gmaps_tries",
        "start_date",
        "location",
        "artist",
        "created",
        "updated",
    ]
    search_fields = ["pk", "name", "slug"]

    def artist(self, obj):
        return obj.artists.first()


admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin
