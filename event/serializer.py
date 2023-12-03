from rest_framework import serializers

from .models import Artist, Event, Location, GMapsLocation, Metadata


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


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = [
            "wiki_page_id",
            "wiki_title",
            "wiki_description",
            "website",
            "image",
            "twitter",
            "facebook",
            "youtube",
            "instagram",
            "tiktok",
            "soundcloud",
            "spotify",
            "appleMusic",
            "email",
            "title",
            "description",
            "type",
        ]

    def create(self, validated_data):
        artist_pk = self.context["request"].data.get("artist")
        location_pk = self.context["request"].data.get("location")

        instance, _ = Metadata.objects.update_or_create(**validated_data)

        if artist_pk:
            artist = Artist.objects.get(pk=artist_pk)
            artist.wiki_tries = artist.wiki_tries + 1
            artist.metadata = instance
            artist.save()

        if location_pk:
            location = Location.objects.get(pk=location_pk)
            location.wiki_tries = location.wiki_tries + 1
            location.metadata = instance
            location.save()

        return instance


class LocationSerializer(serializers.ModelSerializer):
    gmaps = GMapsLocationSerializer(required=False)
    gmaps_tries = serializers.IntegerField(read_only=True)
    metadata = MetadataSerializer(read_only=True)

    class Meta:
        model = Location
        fields = [
            "pk",
            "name",
            "address",
            "city",
            "state",
            "gmaps",
            "gmaps_tries",
            "wiki_tries",
            "metadata",
        ]

    def update(self, instance, validated_data):
        if "wiki_tries" in validated_data:
            instance.wiki_tries = instance.wiki_tries + 1
        else:
            instance.gmaps_tries = instance.gmaps_tries + 1

        instance.save()

        return instance


class ArtistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    metadata = MetadataSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = [
            "pk",
            "name",
            "wiki_tries",
            "metadata",
        ]

    def create(self, validated_data):
        artist, _ = Artist.objects.update_or_create(**validated_data)

        return artist

    def update(self, instance, validated_data):
        instance.wiki_tries = instance.wiki_tries + 1
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)
    artist = ArtistSerializer(required=False, read_only=True)
    name = serializers.CharField(required=True, write_only=True)

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
            "artist",
            "pk",
        ]

    def create(self, validated_data):
        location, _ = Location.objects.update_or_create(
            name=validated_data["location"]["name"],
            address=validated_data["location"].get("address", ""),
            city=validated_data["location"]["city"],
            state=validated_data["location"]["state"],
        )

        artist, _ = Artist.objects.update_or_create(name=validated_data["name"])

        event, _ = Event.objects.update_or_create(
            description=validated_data.get("description", ""),
            image=validated_data["image"],
            url=validated_data["url"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            location=location,
            artist=artist,
        )

        return event
