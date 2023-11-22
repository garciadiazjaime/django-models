from rest_framework import generics
from rest_framework import mixins
from django_filters import rest_framework as filters

from .models import Event, Location, GMapsLocation
from .serializer import EventSerializer, LocationSerializer, GMapsLocationSerializer
from .filters import EventFilter, LocationFilter


class EventViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Event.objects.filter()
    serializer_class = EventSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EventFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LocationViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = Location.objects.filter()
    serializer_class = LocationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = LocationFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class GMapsLocationViewSet(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = GMapsLocation.objects.all()
    serializer_class = GMapsLocationSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
