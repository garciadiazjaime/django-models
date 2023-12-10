from django_filters import rest_framework as filters
from .models import Event, Location, Artist


class EventFilter(filters.FilterSet):
    location_empty = filters.BooleanFilter(field_name="location", method="empty_filter")
    gmaps_tries = filters.NumberFilter(lookup_expr="lt")
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="gte")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Event
        fields = ["location_empty", "gmaps_tries", "start_date"]


class LocationFilter(filters.FilterSet):
    gmaps_empty = filters.BooleanFilter(field_name="gmaps", method="empty_filter")
    metadata_empty = filters.BooleanFilter(field_name="metadata", method="empty_filter")
    gmaps_tries = filters.NumberFilter(lookup_expr="lt")
    wiki_tries = filters.NumberFilter(lookup_expr="lt")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Location
        fields = [
            "gmaps_empty",
            "gmaps_tries",
            "metadata_empty",
            "wiki_tries",
            "slug_venue",
        ]


class ArtistFilter(filters.FilterSet):
    metadata_empty = filters.BooleanFilter(field_name="metadata", method="empty_filter")
    wiki_tries = filters.NumberFilter(lookup_expr="lt")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Artist
        fields = ["metadata_empty", "wiki_tries"]
