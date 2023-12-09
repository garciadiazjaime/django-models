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


# class LocationSerializer(serializers.ModelSerializer):
#     gmaps = GMapsLocationSerializer(required=False)
#     gmaps_tries = serializers.IntegerField(read_only=True)
#     metadata = MetadataSerializer(read_only=True)

#     class Meta:
#         model = Location
#         fields = [
#             "pk",
#             "name",
#             "address",
#             "city",
#             "state",
#             "gmaps",
#             "gmaps_tries",
#             "wiki_tries",
#             "metadata",
#         ]

#     def update(self, instance, validated_data):
#         if "wiki_tries" in validated_data:
#             instance.wiki_tries = instance.wiki_tries + 1
#         else:
#             instance.gmaps_tries = instance.gmaps_tries + 1

#         instance.save()

#         return instance


# class ArtistSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=False)
#     metadata = MetadataSerializer(read_only=True)

#     class Meta:
#         model = Artist
#         fields = [
#             "pk",
#             "name",
#             "wiki_tries",
#             "metadata",
#         ]

#     def create(self, validated_data):
#         artist, _ = Artist.objects.update_or_create(**validated_data)

#         return artist

#     def update(self, instance, validated_data):
#         instance.wiki_tries = instance.wiki_tries + 1
#         instance.save()
#         return instance


class EventSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    # location = LocationSerializer(required=False)
    # artist = ArtistSerializer(required=False, read_only=True)

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
        ]

    def create(self, validated_data):
        event, _ = Event.objects.update_or_create(**validated_data)

        return event


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
