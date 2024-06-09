from datetime import datetime, timedelta, date
from pathlib import Path
import boto3
import json


from django.core.management.base import BaseCommand
from django.core import serializers

from event.models import Event


class Command(BaseCommand):
    def handle(self, **options):
        Path("./data").mkdir(parents=True, exist_ok=True)

        print(f"exporting data {str(date.today())}")
        events = Event.objects.filter(
            created__gt=datetime.now() - timedelta(days=30)
        ).order_by("created")

        created = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        data = serializers.serialize("json", events)
        output = {"created": created, "data": json.loads(data)}

        s3 = boto3.resource("s3")
        s3.Bucket("cmc.data").put_object(
            Key="data/report_last_30_days_events.json",
            Body=bytes(json.dumps(output).encode("UTF-8")),
            ContentType="application/json",
        )
        print(f"{events.count()} events exported")
        print("export completed")
