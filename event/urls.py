from rest_framework import routers, serializers, viewsets
from .models import Event

class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
          'name',
          'description',
          'image',
          'url',
          'start_date',
          'end_date',
          # 'location',
          # 'organizer',
          'sha',
        ]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
