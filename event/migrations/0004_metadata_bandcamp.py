# Generated by Django 4.2.6 on 2024-02-05 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_event_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadata',
            name='bandcamp',
            field=models.URLField(blank=True, default=''),
        ),
    ]
