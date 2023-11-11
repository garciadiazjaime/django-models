from rest_framework import serializers

from .models import Event, Location, Address, Organizer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "locality", "postal", "city", "state"]


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ["name"]


class LocationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Location
        fields = ["name", "url", "telephone", "address"]


class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(required=False)
    location = LocationSerializer()

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

    def create(self, validated_data):
        address = validated_data["location"]["address"]
        locality = address.pop("locality", "")
        postal = address.pop("postal", "")
        address, _ = Address.objects.get_or_create(
            street=address["street"],
            locality=locality,
            postal=postal,
            city=address["city"],
            state=address["state"],
        )

        location, _ = Location.objects.get_or_create(
            name=validated_data["location"]["name"],
            url=validated_data["location"]["url"],
            telephone=validated_data["location"]["telephone"],
            address=address,
        )

        organizer = validated_data.pop("organizer", None)
        if organizer:
            organizer, _ = Organizer.objects.get_or_create(name=organizer["name"])

        event, _ = Event.objects.get_or_create(
            name=validated_data["name"],
            description=validated_data["description"],
            image=validated_data["image"],
            url=validated_data["url"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            location=location,
            organizer=organizer,
        )

        return event
