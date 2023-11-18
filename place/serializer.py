from rest_framework import serializers

from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "pk",
            "lat",
            "lng",
            "name",
            "photo_reference",
            "image",
            "place_id",
            "price_level",
            "rating",
            "types",
            "user_ratings_total",
            "vicinity",
            "website",
            "permanently_closed",
            "gmaps_tries",
        ]

    def create(self, validated_data):
        instance, _ = Place.objects.update_or_create(
            place_id=validated_data["place_id"], defaults=validated_data
        )

        return instance

    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.gmaps_tries = instance.gmaps_tries + 1
        instance.save()

        return instance
