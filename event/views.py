from rest_framework import generics
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from django.utils import timezone


from .models import Event, Location, Artist, Metadata, Spotify
from .serializer import (
    EventSerializer,
    LocationSerializer,
    MetadataSerializer,
    ArtistSerializer,
    SpotifySerializer,
)
from .filters import EventFilter, LocationFilter, ArtistFilter, MetadataFilter


class EventViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ["rank"]

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

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
    ordering_fields = ["metadata__spotify__tries"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ArtistMetadataViewSet(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    queryset = Artist.objects.filter(
        event__start_date__gt=timezone.now(),
        event__location__isnull=False,
        spotify__genres__isnull=False,
    ).distinct()
    serializer_class = ArtistSerializer

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
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = Spotify.objects.all()
    serializer_class = SpotifySerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
