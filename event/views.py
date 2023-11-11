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
        address, _ = Address.objects.get_or_create(request.data["location"]["address"])

        location = request.data["location"]
        location, _ = Location.objects.get_or_create(
            name=location["name"],
            url=location["url"],
            telephone=location["telephone"],
            address=address,
        )

        organizer, _ = Organizer.objects.get_or_create(request.data["organizer"])

        payload = dict(
            name=request.data["name"],
            description=request.data["description"],
            image=request.data["image"],
            url=request.data["url"],
            start_date=request.data["start_date"],
            end_date=request.data["end_date"],
            location=location.pk,
            organizer=organizer.pk,
        )

        serializer = EventSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
