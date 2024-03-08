from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Event, Location, Artist, Metadata, Slug


class EventFilter(filters.FilterSet):
    location_empty = filters.BooleanFilter(field_name="location", method="empty_filter")
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="start_date", lookup_expr="lte")
    artist_empty = filters.BooleanFilter(field_name="artists", method="empty_filter")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Event
        fields = ["location_empty", "start_date", "end_date", "provider"]


class LocationFilter(filters.FilterSet):
    gmaps_empty = filters.BooleanFilter(field_name="gmaps", method="empty_filter")

    metadata_empty = filters.BooleanFilter(field_name="metadata", method="empty_filter")

    website_empty = filters.BooleanFilter(field_name="website", method="empty_filter")

    slug_venue = filters.CharFilter(field_name="slug_venue", method="slug_venue_filter")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    def slug_venue_filter(self, queryset, name, value):
        return queryset.filter(slug_venue__name=value)

    class Meta:
        model = Location
        fields = [
            "gmaps_empty",
            "metadata_empty",
            "slug_venue",
        ]


class ArtistFilter(filters.FilterSet):
    spotify_empty = filters.BooleanFilter(method="spotify_empty_filter")
    spotify_genres_empty = filters.BooleanFilter(method="spotify_genres_empty_filter")

    def spotify_genres_empty_filter(self, queryset, name, value):
        return queryset.filter(metadata__spotify__genres__isnull=value)

    def spotify_empty_filter(self, queryset, name, value):
        return queryset.filter(metadata__spotify__isnull=value)

    class Meta:
        model = Artist
        fields = ["spotify_empty", "spotify_genres_empty", "slug"]


class MetadataFilter(filters.FilterSet):
    spotify_empty = filters.BooleanFilter(field_name="spotify", method="empty_filter")

    def empty_filter(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: ""})

        return queryset.filter(~Q(**{name: ""}))

    class Meta:
        model = Metadata
        fields = ["spotify_empty", "type"]
