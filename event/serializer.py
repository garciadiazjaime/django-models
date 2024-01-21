from rest_framework import serializers

from .models import Artist, Event, Location, Metadata, Spotify, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class SpotifySerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Spotify
        fields = ["pk", "followers", "genres", "popularity", "url", "tries"]


class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = [
            "pk",
            "website",
            "image",
            "twitter",
            "facebook",
            "youtube",
            "instagram",
            "tiktok",
            "soundcloud",
            # "spotify",
            "appleMusic",
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

            spotify = None
            if "spotify_url" in validated_data:
                spotify_url = validated_data.pop("spotify_url")
                spotify, _ = Spotify.objects.update_or_create(url=spotify_url)

            instance, _ = Metadata.objects.update_or_create(
                slug=slug, spotify=spotify, defaults=validated_data
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
    metadata = MetadataSerializer()

    class Meta:
        model = Location
        fields = [
            "pk",
            "name",
            "address",
            "lat",
            "lng",
            "place_id",
            "website",
            "slug_venue",
            "metadata",
        ]


class ArtistSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(required=False)

    class Meta:
        model = Artist
        fields = ["pk", "name", "profile", "metadata"]


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


class EventProcessedSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    artists = ArtistSerializer(required=False, many=True)

    class Meta:
        model = Event
        fields = [
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
            "location",
            "artists",
        ]

    def create(self, validated_data):
        pre_location = validated_data.pop("location")
        pre_location_meta = (
            pre_location.pop("metadata") if "metadata" in pre_location else None
        )
        pre_artists = (
            validated_data.pop("artists") if "artists" in validated_data else None
        )

        location, _ = Location.objects.update_or_create(**pre_location)

        if pre_location_meta:
            location_meta, _ = Metadata.objects.update_or_create(
                type="LOCATION", slug=location.slug, **pre_location_meta
            )

            location.metadata = location_meta
            location.save()

        instance, _ = Event.objects.update_or_create(
            location=location, **validated_data
        )

        for pre_artist in pre_artists:
            pre_artist_meta = (
                pre_artist.pop("metadata") if "metadata" in pre_artist else None
            )

            artist, _ = Artist.objects.update_or_create(**pre_artist)

            if pre_artist_meta:
                artist_meta, _ = Metadata.objects.update_or_create(
                    type="ARTIST", slug=artist.slug, **pre_artist_meta
                )

                artist.metadata = artist_meta
                artist.save()

            instance.artists.add(artist)

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


class SpotifySerializer(serializers.ModelSerializer):
    image = serializers.URLField(write_only=True, required=False)
    genres = serializers.JSONField(write_only=True, required=False)

    class Meta:
        model = Spotify
        fields = [
            "pk",
            "followers",
            "popularity",
            "image",
            "genres",
        ]

    def update(self, instance, validated_data):
        genres = validated_data.get("genres")
        if genres:
            for genre in genres:
                instance_genre, _ = Genre.objects.update_or_create(name=genre)
                instance.genres.add(instance_genre)

        instance.followers = validated_data.get("followers", instance.followers)
        instance.popularity = validated_data.get("popularity", instance.popularity)
        instance.image = validated_data.get("image", instance.image)
        instance.tries = instance.tries + 1
        instance.save()

        return instance
