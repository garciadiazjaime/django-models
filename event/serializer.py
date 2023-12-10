from rest_framework import serializers

from .models import Artist, Event, Location, Metadata

from .misc import get_performer


# class GMapsLocationSerializer(serializers.ModelSerializer):
#     location = serializers.PrimaryKeyRelatedField(
#         queryset=Location.objects.all(), write_only=True, required=True
#     )
#     lat = serializers.FloatField()
#     lng = serializers.FloatField()

#     class Meta:
#         model = GMapsLocation
#         fields = ["lat", "lng", "formatted_address", "name", "place_id", "location"]

#     def create(self, validated_data):
#         location = validated_data.get("location")

#         instance, _ = GMapsLocation.objects.update_or_create(
#             slug=location.slug, defaults=validated_data
#         )

#         location.gmaps = instance
#         location.gmaps_tries = location.gmaps_tries + 1
#         location.save()

#         return instance


# class MetadataSerializer(serializers.ModelSerializer):
#     artist = serializers.PrimaryKeyRelatedField(
#         queryset=Artist.objects.all(), write_only=True, required=False
#     )
#     location = serializers.PrimaryKeyRelatedField(
#         queryset=Location.objects.all(), write_only=True, required=False
#     )

#     class Meta:
#         model = Metadata
#         fields = [
#             "wiki_page_id",
#             "wiki_title",
#             "wiki_description",
#             "website",
#             "image",
#             "twitter",
#             "facebook",
#             "youtube",
#             "instagram",
#             "tiktok",
#             "soundcloud",
#             "spotify",
#             "appleMusic",
#             "email",
#             "title",
#             "description",
#             "type",
#             "artist",
#             "location",
#         ]

#     def create(self, validated_data):
#         artist = validated_data.get("artist")
#         location = validated_data.get("location")

#         if artist:
#             instance, _ = Metadata.objects.update_or_create(
#                 slug=artist.slug, defaults=validated_data
#             )

#             artist.wiki_tries = artist.wiki_tries + 1
#             artist.metadata = instance
#             artist.save()

#         if location:
#             instance, _ = Metadata.objects.update_or_create(
#                 slug=location.slug, defaults=validated_data
#             )

#             location.wiki_tries = location.wiki_tries + 1
#             location.metadata = instance
#             location.save()

#         return instance


class LocationSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), write_only=True
    )
    # gmaps = GMapsLocationSerializer(required=False)
    # gmaps_tries = serializers.IntegerField(read_only=True)
    # metadata = MetadataSerializer(read_only=True)

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

    # def update(self, instance, validated_data):
    #     if "wiki_tries" in validated_data:
    #         instance.wiki_tries = instance.wiki_tries + 1
    #     else:
    #         instance.gmaps_tries = instance.gmaps_tries + 1

    #     instance.save()

    #     return instance


class ArtistSerializer(serializers.ModelSerializer):
    # metadata = MetadataSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = [
            "name",
        ]

    # def create(self, validated_data):
    #     artist, _ = Artist.objects.update_or_create(**validated_data)

    #     return artist

    # def update(self, instance, validated_data):
    #     instance.wiki_tries = instance.wiki_tries + 1
    #     instance.save()
    #     return instance


class EventSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    gmaps_tries = serializers.IntegerField(required=False)
    location = LocationSerializer(read_only=True)
    location_pk = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), write_only=True, required=False
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
            "location",
            "artists",
            "pk",
            "location_pk",
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

        return instance


# class EventRankSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source="artist.name", read_only=True)

#     class Meta:
#         model = Event
#         fields = [
#             "name",
#             "rank",
#             "start_date",
#             "pk",
#         ]

#     def create(self, validated_data):
#         for event in Event.objects.filter(start_date__gte=validated_data["start_date"]):
#             rank = 0
#             metadata = event.location.metadata
#             if metadata:
#                 if (
#                     metadata.twitter
#                     or metadata.facebook
#                     or metadata.youtube
#                     or metadata.instagram
#                     or metadata.tiktok
#                 ):
#                     rank += 100

#                 if metadata.soundcloud or metadata.spotify or metadata.appleMusic:
#                     rank += 1000

#             metadata = event.artist.metadata
#             if metadata:
#                 if (
#                     metadata.twitter
#                     or metadata.facebook
#                     or metadata.youtube
#                     or metadata.instagram
#                     or metadata.tiktok
#                 ):
#                     rank += 100

#                 if metadata.soundcloud or metadata.spotify or metadata.appleMusic:
#                     rank += 1000

#             event.rank = rank
#             event.save()

#         return Event.objects.order_by("-rank").first()
