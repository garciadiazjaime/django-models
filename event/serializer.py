from datetime import datetime, time
import pytz
from rest_framework import serializers
from rest_framework.serializers import FloatField

from event.models import Artist, Event, Location, Metadata, Spotify, Genre, Slug, MusicO
from event.support import get_rank, get_location_rank


class SlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slug
        fields = ["name"]


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
    slug = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = Metadata
        fields = [
            "pk",
            "slug",
            "type",
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
            "band_camp",
            "link_tree",
        ]


class GenerativeMetadataSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(required=False, allow_null=True)
    subgenre = serializers.CharField(required=False, allow_null=True)
    type = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Metadata
        fields = ["genre", "subgenre", "type"]


class LocationSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    metadata = MetadataSerializer(required=False, allow_null=True)
    slug = serializers.CharField(read_only=True)
    slug_venue = SlugSerializer(many=True)

    class Meta:
        model = Location
        fields = [
            "pk",
            "name",
            "slug",
            "address",
            "lat",
            "lng",
            "place_id",
            "website",
            "url",
            "slug_venue",
            "metadata",
            "provider",
        ]


class MusicOSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = MusicO
        fields = [
            "pk",
            "followers",
            "popularity",
            "image",
            "genres",
            "artist",
        ]


class ArtistSerializer(serializers.ModelSerializer):
    metadata = MetadataSerializer(required=False, allow_null=True)
    spotify = SpotifySerializer(required=False, allow_null=True)
    genres = GenreSerializer(many=True, required=False, allow_null=True)
    musicO = MusicOSerializer(required=False, allow_null=True)

    class Meta:
        model = Artist
        fields = [
            "pk",
            "name",
            "profile",
            "popularity",
            "metadata",
            "spotify",
            "genres",
            "musicO",
            "slug",
        ]

    def create(self, validated_data):
        pre_music_o = (
            validated_data.pop("musicO") if "musicO" in validated_data else None
        )
        pre_artist_meta = (
            validated_data.pop("metadata") if "metadata" in validated_data else None
        )
        pre_artist_spotify = (
            validated_data.pop("spotify") if "spotify" in validated_data else None
        )
        pre_artist_genres = (
            validated_data.pop("genres") if "genres" in validated_data else None
        )
        pre_artist_slug = validated_data.pop("slug")

        instance, _ = Artist.objects.update_or_create(
            slug=pre_artist_slug, defaults=validated_data
        )

        if pre_artist_meta:
            artist_meta, _ = Metadata.objects.update_or_create(
                type="ARTIST", slug=instance.slug, defaults=pre_artist_meta
            )

            instance.metadata = artist_meta
            instance.save()

        if pre_artist_spotify:
            pre_spotify_genres = (
                pre_artist_spotify.pop("genres")
                if "genres" in pre_artist_spotify
                else None
            )
            artist_spotify, _ = Spotify.objects.update_or_create(
                url=pre_artist_spotify["url"], defaults=pre_artist_spotify
            )
            instance.spotify = artist_spotify
            instance.save()

            for pre_genre in pre_spotify_genres:
                genre, _ = Genre.objects.update_or_create(**pre_genre)
                artist_spotify.genres.add(genre)

        if pre_artist_genres:
            for pre_genre in pre_artist_genres:
                genre, _ = Genre.objects.update_or_create(**pre_genre)
                instance.genres.add(genre)

        if pre_music_o:
            pre_music_o_genres = (
                pre_music_o.pop("genres") if "genres" in pre_music_o else None
            )
            music_o, _ = MusicO.objects.update_or_create(
                artist=instance, defaults=pre_music_o
            )

            for pre_genre in pre_music_o_genres:
                genre, _ = Genre.objects.update_or_create(**pre_genre)
                music_o.genres.add(genre)

        return instance


class BlankFloatField(FloatField):
    """
    This accepts an empty string as None
    """

    def to_internal_value(self, data):
        if data == "":
            return None
        return super().to_internal_value(data)


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    artists = ArtistSerializer(required=False, many=True)
    rank = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)
    price = BlankFloatField(required=False, allow_null=True, default=None)
    generativemetadata_set = GenerativeMetadataSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = [
            "pk",
            "rank",
            "slug",
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
            "price",
            "buyUrl",
            "location",
            "artists",
            "generativemetadata_set",
        ]

    def create(self, validated_data):
        pre_location = validated_data.pop("location")
        pre_location_meta = (
            pre_location.pop("metadata") if "metadata" in pre_location else None
        )
        pre_artists = (
            validated_data.pop("artists") if "artists" in validated_data else []
        )
        pre_location_slug_venue = (
            pre_location.pop("slug_venue") if "slug_venue" in pre_location else []
        )

        place_id = pre_location.pop("place_id")
        location, _ = Location.objects.update_or_create(
            place_id=place_id, defaults=pre_location
        )

        for pre_location_slug in pre_location_slug_venue:
            slug, _ = Slug.objects.get_or_create(**pre_location_slug)
            location.slug_venue.add(slug)

        if pre_location_meta:
            location_meta, _ = Metadata.objects.update_or_create(
                type="LOCATION", slug=location.slug, **pre_location_meta
            )

            location.metadata = location_meta
            location.rank = get_location_rank(pre_location_meta)
            location.save()
        instance, _ = Event.objects.update_or_create(
            url=validated_data["url"],
            start_date=validated_data["start_date"],
            location=location,
            defaults=validated_data,
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
            pre_artist_slug = pre_artist.pop("slug")

            artist, _ = Artist.objects.update_or_create(
                slug=pre_artist_slug, defaults=pre_artist
            )

            if pre_artist_meta:
                artist_meta, _ = Metadata.objects.update_or_create(
                    type="ARTIST", slug=artist.slug, defaults=pre_artist_meta
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
