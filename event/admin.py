from django.contrib import admin
from django.db.models import Count

from .models import Location, Event, Artist, Metadata, Spotify, Genre


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
        "slug_venue",
        "events",
        "metadata",
        "created",
        "updated",
        "pk",
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
        "rank",
        "url",
        "location",
        "artist",
        "provider",
        "start_date",
        "updated",
        "pk",
    ]
    search_fields = ["pk", "name", "slug", "venue", "provider"]

    def artist(self, obj):
        return [artist.name for artist in obj.artists.all()]

    def location_pk(self, obj):
        if obj.location:
            return obj.location.pk


admin.site.register(Genre, GenreAdmin)
admin.site.register(Spotify, SpotifyAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Event, EventAdmin)

from django.contrib import admin
