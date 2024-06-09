from datetime import datetime, timedelta, date

from django.core.management.base import BaseCommand
from event.models import Event
from pathlib import Path
import boto3
import json
from django.core import serializers


class Command(BaseCommand):
    def handle(self, **options):
        Path("./data").mkdir(parents=True, exist_ok=True)

        print(f"exporting data {str(date.today())}")
        events = Event.objects.filter(
            created__gt=datetime.now() - timedelta(days=30)
        ).order_by("created")

        data = serializers.serialize("json", events)

        s3 = boto3.resource("s3")
        s3.Bucket("cmc.data").put_object(
            Key="report_last_30_days_events.json", Body=json.dumps(data)
        )
        print(f"{events.count()} events exported")
        print("export completed")
