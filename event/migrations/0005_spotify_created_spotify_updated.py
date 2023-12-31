# Generated by Django 4.2.6 on 2023-12-22 23:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_spotify_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='spotify',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spotify',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
