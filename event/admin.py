from django.contrib import admin
from django.db.models import Count

from .models import Location, Event, Artist, Metadata, Spotify


class SpotifyAdmin(admin.ModelAdmin):
    list_display = ["artist", "tries", "genres_list", "followers", "popularity", "url"]

    def genres_list(self, obj):
        return ",".join(obj.genres.all())

    def artist(self, obj):
        return obj.metadata_set.first().artist_set.first()


class MetadataAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "type",
        "ref",
        "social",
        "music",
        "website",
        "spotify",
        "created",
        "updated",
    ]
    search_fields = ["slug"]

    def ref(self, obj):
        if obj.location_set.count():
            return "location"

        if obj.artist_set.count():
            return "artist"

        return None

    def social(self, obj):
        if obj.twitter or obj.facebook or obj.instagram or obj.tiktok:
            return True

        return False

    def music(self, obj):
        if obj.youtube or obj.soundcloud or obj.spotify or obj.appleMusic:
            return True

        return False


class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "slug_venue",
        "events",
        "metadata",
        "meta_tries",
        "pk",
        "created",
        "updated",
    ]
    search_fields = ["name", "pk"]

    def get_queryset(self, request):
        qs = super(LocationAdmin, self).get_queryset(request)
        qs = qs.annotate(events=Count("event"))
        return qs

    def events(self, obj):
        return obj.event_set.count()

    events.admin_order_field = "events"


class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "profile",
        "events",
        "created",
        "updated",
    ]
    search_fields = ["name"]

    def events(self, obj):
        return obj.event_set.count()


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "venue",
        "url",
        "gmaps_tries",
        "artist_tries",
        "location_pk",
        "location",
        "artist",
        "provider",
        "start_date",
        "created",
        "updated",
        "pk",
    ]
    search_fields = ["pk", "name", "slug", "venue"]

    def artist(self, obj):
        return [artist.name for artist in obj.artists.all()]

    def location_pk(self, obj):
        if obj.location:
            return obj.location.pk


admin.site.register(Spotify, SpotifyAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin
