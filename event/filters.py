from django_filters import rest_framework as filters
from .models import Event, Location, Artist


class EventFilter(filters.FilterSet):
    gmaps_empty = filters.CharFilter(method="gmaps_empty_filter")
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="gte")

    def gmaps_empty_filter(self, queryset, name, value):
        value = value.lower() == "true"
        return queryset.filter(location__gmaps__isnull=value)

    class Meta:
        model = Event
        fields = ["gmaps_empty", "start_date"]


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
        fields = ["gmaps_empty", "gmaps_tries", "metadata_empty", "wiki_tries"]


class ArtistFilter(filters.FilterSet):
    metadata_empty = filters.BooleanFilter(field_name="metadata", method="empty_filter")
    wiki_tries = filters.NumberFilter(lookup_expr="lt")

    def empty_filter(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Artist
        fields = ["metadata_empty", "wiki_tries"]
