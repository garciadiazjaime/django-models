from rest_framework import serializers

from .models import Event, Location, GMapsLocation


class GMapsLocationSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

    class Meta:
        model = GMapsLocation
        fields = ["lat", "lng", "formatted_address", "name", "place_id"]

    def create(self, validated_data):
        location_pk = self.context["request"].data["location"]
        location = Location.objects.get(pk=location_pk)

        instance, _ = GMapsLocation.objects.update_or_create(**validated_data)

        location.gmaps = instance
        location.gmaps_tries = location.gmaps_tries + 1
        location.save()

        return instance


class LocationSerializer(serializers.ModelSerializer):
    gmaps = GMapsLocationSerializer(required=False)
    gmaps_tries = serializers.IntegerField(read_only=True)
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = Location
        fields = ["name", "address", "city", "state", "gmaps", "gmaps_tries", "pk"]

    def update(self, instance, validated_data):
        instance.gmaps_tries = instance.gmaps_tries + 1
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

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
            "pk",
        ]

    def create(self, validated_data):
        location, _ = Location.objects.update_or_create(
            name=validated_data["location"]["name"],
            address=validated_data["location"].get("address", ""),
            city=validated_data["location"]["city"],
            state=validated_data["location"]["state"],
        )

        event, _ = Event.objects.update_or_create(
            name=validated_data["name"],
            description=validated_data.get("description", ""),
            image=validated_data["image"],
            url=validated_data["url"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            location=location,
        )

        return event
