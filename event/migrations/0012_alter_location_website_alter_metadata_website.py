# Generated by Django 4.2.6 on 2024-07-22 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_alter_event_buyurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='website',
            field=models.URLField(blank=True, default='', max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='website',
            field=models.URLField(blank=True, default='', max_length=240),
        ),
    ]
