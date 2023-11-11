from rest_framework.response import Response
from rest_framework import generics


from rest_framework import mixins
from rest_framework import status


from .models import Event, Location, Address, Organizer


from .serializer import EventSerializer


class EventViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
