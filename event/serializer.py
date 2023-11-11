from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "image",
            "url",
            "start_date",
            "end_date",
            "location",
            "organizer",
        ]
