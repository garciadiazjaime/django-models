# Generated by Django 4.2.6 on 2024-01-26 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_remove_event_artist_tries_remove_event_gmaps_tries_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='website',
            field=models.URLField(default='', null=True),
        ),
    ]