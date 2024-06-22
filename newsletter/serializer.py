from rest_framework import serializers

from newsletter.models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["email"]

    def create(self, validated_data):
        instance, _ = Subscriber.objects.update_or_create(defaults=validated_data)
        return instance
