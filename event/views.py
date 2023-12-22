from rest_framework import generics
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters


from .models import Event, Location, Artist, Metadata, Spotify
from .serializer import (
    EventSerializer,
    LocationSerializer,
    MetadataSerializer,
    ArtistSerializer,
    EventRankSerializer,
    SpotifySerializer,
)
from .filters import EventFilter, LocationFilter, ArtistFilter, MetadataFilter


class EventViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ["rank", "gmaps_tries"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class EventRankViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Event.objects.all()
    serializer_class = EventRankSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LocationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = LocationFilter
    ordering_fields = ["wiki_tries"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArtistViewSet(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ArtistFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MetadataViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = MetadataFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SpotifyViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Spotify.objects.all()
    serializer_class = SpotifySerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
