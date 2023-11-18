from django_filters import rest_framework as filters
from .models import Place


class PlaceFilter(filters.FilterSet):

    """Filter for Books by if books are published or not"""

    image_empty = filters.CharFilter(field_name="image", method="boolean_filter")
    gmaps_tries_lower = filters.NumberFilter(
        field_name="gmaps_tries", method="lower_filter"
    )

    def boolean_filter(self, queryset, name, value):
        value = value.lower() == "true"
        lookup = "__".join([name, "isnull"])
        return queryset.filter(**{lookup: value})

    def lower_filter(self, queryset, name, value):
        lookup = "__".join([name, "lt"])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Place
        fields = ["image_empty"]
