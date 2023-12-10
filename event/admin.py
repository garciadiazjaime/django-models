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
    list_display = ["name", "slug", "slug_venue", "lat", "lng", "created", "updated"]
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
        "venue",
        "gmaps_tries",
        "location_pk",
        "location",
        "artist",
        "start_date",
        "created",
        "updated",
    ]
    search_fields = ["pk", "name", "slug", "venue"]

    def artist(self, obj):
        return obj.artists.first()

    def location_pk(self, obj):
        if obj.location:
            return obj.location.pk


admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin
