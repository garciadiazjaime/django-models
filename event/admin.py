from django.contrib import admin
from django.db.models import Count

from .models import (
    Location,
    Event,
    Artist,
    Metadata,
    Spotify,
    Genre,
    Slug,
    MusicO,
    Twitter,
)


class SlugAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created",
        "updated",
    ]
    search_fields = ["name"]


class GenreAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "artists",
        "created",
        "updated",
    ]
    search_fields = ["name"]

    def artists(self, obj):
        return obj.spotify_set.count()


class SpotifyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "genres_list",
        "followers",
        "popularity",
        "url",
        "image",
        "created",
        "updated",
    ]
    search_fields = ["name"]

    def genres_list(self, obj):
        return ",".join(obj.genres.values_list("name", flat=True))


class MetadataAdmin(admin.ModelAdmin):
    list_display = [
        "slug",
        "youtube",
        "website",
        "type",
        "social",
        "music",
        "spotify",
        "image",
        "created",
        "updated",
    ]
    search_fields = ["slug"]

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
        "rank",
        "events",
        "has_metadata",
        "provider",
        "sources",
        "updated",
        "place_id",
        "address",
        "lat",
        "lng",
        "pk",
    ]
    search_fields = ["name", "pk", "address", "lat", "lng"]

    def get_queryset(self, request):
        qs = super(LocationAdmin, self).get_queryset(request)
        qs = qs.annotate(events=Count("event"))
        return qs

    def events(self, obj):
        return obj.event_set.count()

    def has_metadata(self, obj):
        return 1 if obj.metadata else 0

    def sources(self, obj):
        return ", ".join(
            obj.event_set.all().values_list("provider", flat=True).distinct()
        )

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
        "rank",
        "url",
        "venue",
        "location",
        "location_pk",
        "location_id",
        "artist",
        "artist_count",
        "provider",
        "start_date",
        "updated",
        "pk",
    ]
    search_fields = ["pk", "name", "slug", "venue", "provider"]

    def artist(self, obj):
        return [artist.name for artist in obj.artists.all()]

    def artist_count(self, obj):
        return obj.artists.count()

    def location_pk(self, obj):
        if obj.location:
            return obj.location.pk

    def location_id(self, obj):
        return obj.location.place_id


class MusicOAdmin(admin.ModelAdmin):
    list_display = [
        "artist",
        "events",
        "followers",
        "popularity",
        "genres_list",
        "image",
        "created",
        "updated",
    ]
    search_fields = ["artist__name"]

    def events(self, obj):
        return obj.artist.event_set.count()

    def genres_list(self, obj):
        return ",".join(obj.genres.values_list("name", flat=True))


class TwitterAdmin(admin.ModelAdmin):
    list_display = [
        "handler",
        "url",
        "followers_count",
        "friends_count",
        "image",
        "artist",
        "created",
        "updated",
    ]

    def url(sef, obj):
        return obj.artist.metadata.twitter


admin.site.register(Genre, GenreAdmin)
admin.site.register(Spotify, SpotifyAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Slug, SlugAdmin)

admin.site.register(MusicO, MusicOAdmin)
admin.site.register(Twitter, TwitterAdmin)


from django.contrib import admin
