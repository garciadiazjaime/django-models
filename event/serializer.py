from rest_framework import serializers

from .models import Artist, Event, Location, Metadata, Spotify, Genre
from .support import get_rank


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class SpotifySerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Spotify
        fields = [
            "pk",
            "name",
            "followers",
            "genres",
            "popularity",
            "url",
            "image",
        ]


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
            "spotify",
            "appleMusic",
        ]


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
    metadata = MetadataSerializer(required=False, allow_null=True)
    spotify = SpotifySerializer(required=False, allow_null=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Artist
        fields = ["pk", "name", "profile", "metadata", "spotify", "genres"]


class EventSerializer(serializers.ModelSerializer):
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
            validated_data.pop("artists") if "artists" in validated_data else []
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
            pre_artist_spotify = (
                pre_artist.pop("spotify") if "spotify" in pre_artist else None
            )
            pre_artist_genres = (
                pre_artist.pop("genres") if "genres" in pre_artist else None
            )

            artist, _ = Artist.objects.update_or_create(**pre_artist)

            if pre_artist_meta:
                artist_meta, _ = Metadata.objects.update_or_create(
                    type="ARTIST", slug=artist.slug, **pre_artist_meta
                )

                artist.metadata = artist_meta
                artist.save()

            if pre_artist_spotify:
                pre_spotify_genres = (
                    pre_artist_spotify.pop("genres")
                    if "genres" in pre_artist_spotify
                    else None
                )
                artist_spotify, _ = Spotify.objects.update_or_create(
                    **pre_artist_spotify
                )
                artist.spotify = artist_spotify
                artist.save()

                for pre_genre in pre_spotify_genres:
                    genre, _ = Genre.objects.update_or_create(**pre_genre)
                    artist_spotify.genres.add(genre)

            if pre_artist_genres:
                for pre_genre in pre_artist_genres:
                    genre, _ = Genre.objects.update_or_create(**pre_genre)
                    artist.genres.add(genre)

            instance.artists.add(artist)

        instance.rank = get_rank(instance)
        instance.save()

        return instance
