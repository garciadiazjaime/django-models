from rest_framework import serializers

from newsletter.models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance, _ = Subscriber.objects.update_or_create(defaults=validated_data)
        return instance
