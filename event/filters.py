from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Event, Location, Artist, Metadata


class EventFilter(filters.FilterSet):
    location_empty = filters.BooleanFilter(field_name="location", method="empty_filter")
    gmaps_tries = filters.NumberFilter(lookup_expr="lt")
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="gte")
    artist_empty = filters.BooleanFilter(field_name="artists", method="empty_filter")
    artist_tries = filters.NumberFilter(lookup_expr="lt")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Event
        fields = ["location_empty", "gmaps_tries", "start_date", "provider"]


class LocationFilter(filters.FilterSet):
    gmaps_empty = filters.BooleanFilter(field_name="gmaps", method="empty_filter")
    gmaps_tries = filters.NumberFilter(lookup_expr="lt")

    metadata_empty = filters.BooleanFilter(field_name="metadata", method="empty_filter")
    meta_tries = filters.NumberFilter(lookup_expr="lt")

    website_empty = filters.BooleanFilter(field_name="website", method="empty_filter")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Location
        fields = [
            "gmaps_empty",
            "gmaps_tries",
            "metadata_empty",
            "meta_tries",
            "slug_venue",
        ]


class ArtistFilter(filters.FilterSet):
    spotify_empty = filters.BooleanFilter(method="spotify_empty_filter")
    spotify_tries = filters.NumberFilter(method="spotify_tries_filter")
    spotify_genres_empty = filters.BooleanFilter(method="spotify_genres_empty_filter")

    def spotify_genres_empty_filter(self, queryset, name, value):
        return queryset.filter(metadata__spotify__genres__isnull=value)

    def spotify_empty_filter(self, queryset, name, value):
        return queryset.filter(metadata__spotify__isnull=value)

    def spotify_tries_filter(self, queryset, name, value):
        return queryset.filter(metadata__spotify__tries__lt=value)

    class Meta:
        model = Artist
        fields = ["spotify_empty", "spotify_tries", "spotify_genres_empty", "slug"]


class MetadataFilter(filters.FilterSet):
    spotify_empty = filters.BooleanFilter(field_name="spotify", method="empty_filter")

    def empty_filter(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: ""})

        return queryset.filter(~Q(**{name: ""}))

    class Meta:
        model = Metadata
        fields = ["spotify_empty", "type"]
