from rest_framework import generics
from rest_framework import mixins

from newsletter.models import Subscriber
from newsletter.serializer import SubscriberSerializer


class SubscriberViewSet(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
