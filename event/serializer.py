from rest_framework import serializers

from .models import Event, Location, Address, Organizer, GMapsLocation


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "locality", "postal", "city", "state"]


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ["name"]


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
    address = AddressSerializer()
    gmaps = GMapsLocationSerializer(required=False)
    gmaps_tries = serializers.IntegerField(read_only=True)
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = Location
        fields = ["name", "url", "telephone", "address", "gmaps", "gmaps_tries", "pk"]

    def update(self, instance, validated_data):
        instance.gmaps_tries = instance.gmaps_tries + 1
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(required=False)
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
