from rest_framework import serializers

from .models import Artist, Event, Location, Metadata


class MetadataSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), write_only=True, required=False
    )

    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), write_only=True, required=False
    )
    artist = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), write_only=True, required=False
    )
    name = serializers.CharField(write_only=True, required=False)
    profile = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Metadata
        fields = [
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
            "event",
            "artist",
            "location",
            "slug",
            "profile",
            "name",
            "type",
        ]

    def create(self, validated_data):
        event = validated_data.get("event")
        location = validated_data.get("location")

        if location:
            instance, _ = Metadata.objects.update_or_create(
                slug=location.slug, defaults=validated_data
            )

            location.meta_tries = location.meta_tries + 1
            location.metadata = instance
            location.save()

        elif event:
            event = validated_data.pop("event")
            if "profile" not in validated_data:
                event.artist_tries = event.artist_tries + 1
                event.save()

                raise serializers.ValidationError("profile not present")

            slug = validated_data.pop("slug")
            name = validated_data.pop("name")
            profile = validated_data.pop("profile")

            instance, _ = Metadata.objects.update_or_create(
                slug=slug, defaults=validated_data
            )

            artist, _ = Artist.objects.update_or_create(
                name=name, profile=profile, metadata=instance
            )

            event.artists.add(artist)
            event.artist_tries = event.artist_tries + 1
            event.save()

        return instance


class LocationSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    slug = serializers.CharField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), write_only=True
    )
    meta_tries = serializers.IntegerField(required=False)
    metadata = MetadataSerializer(read_only=True)

    class Meta:
        model = Location
        fields = [
            "name",
            "address",
            "lat",
            "lng",
            "place_id",
            "slug",
            "slug_venue",
            "event",
            "pk",
            "meta_tries",
            "website",
            "metadata",
        ]

    def create(self, validated_data):
        event = validated_data.get("event")

        place_id = validated_data.get("place_id")
        instance, _ = Location.objects.update_or_create(
            place_id=place_id, defaults=validated_data
        )

        event.location = instance
        event.gmaps_tries = event.gmaps_tries + 1
        event.save()

        return instance

    def update(self, instance, validated_data):
        if validated_data.get("meta_tries"):
            instance.meta_tries = instance.meta_tries + 1

        return instance


class ArtistSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = ["pk", "name", "slug", "metadata"]


class EventSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    gmaps_tries = serializers.IntegerField(required=False)
    location = LocationSerializer(read_only=True)
    location_pk = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), write_only=True, required=False
    )
    artist_pk = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), write_only=True, required=False
    )
    artists = ArtistSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = [
            "rank",
            "name",
            "description",
            "image",
            "url",
            "start_date",
            "end_date",
            "provider",
            "venue",
            "address",
            "city",
            "slug",
            "gmaps_tries",
            "artist_tries",
            "location",
            "artists",
            "pk",
            "location_pk",
            "artist_pk",
        ]

    def create(self, validated_data):
        instance, _ = Event.objects.update_or_create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        if validated_data.get("gmaps_tries"):
            instance.gmaps_tries = instance.gmaps_tries + 1

            location = validated_data.get("location_pk")
            if location:
                instance.location = location

            instance.save()

        if validated_data.get("artist_tries"):
            instance.artist_tries = instance.artist_tries + 1

            artist = validated_data.get("artist_pk")
            if artist:
                instance.artists.add(artist)

            instance.save()

        return instance


class EventRankSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "name",
            "rank",
            "start_date",
            "pk",
        ]

    def create(self, validated_data):
        for event in Event.objects.filter(
            location__isnull=False, start_date__gte=validated_data["start_date"]
        ):
            rank = 0
            metadata = event.location.metadata
            if metadata:
                if (
                    metadata.twitter
                    or metadata.facebook
                    or metadata.youtube
                    or metadata.instagram
                    or metadata.tiktok
                ):
                    rank += 100

                if metadata.soundcloud or metadata.spotify or metadata.appleMusic:
                    rank += 1000

            for artist in event.artists.all():
                metadata = artist.metadata
                if metadata:
                    if (
                        metadata.twitter
                        or metadata.facebook
                        or metadata.youtube
                        or metadata.instagram
                        or metadata.tiktok
                    ):
                        rank += 100

                    if metadata.soundcloud or metadata.spotify or metadata.appleMusic:
                        rank += 1000

            event.rank = rank
            event.save()

        return Event.objects.order_by("-rank").first()
