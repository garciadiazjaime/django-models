from rest_framework import generics
from rest_framework import mixins

from .models import Event, Location, GMapsLocation
from .serializer import EventSerializer, LocationSerializer, GMapsLocationSerializer


class EventViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Event.objects.filter(location__gmaps__isnull=False)
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LocationViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView
):
    queryset = Location.objects.filter(gmaps__isnull=True, gmaps_tries__lt=3)
    serializer_class = LocationSerializer

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
