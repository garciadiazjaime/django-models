# Generated by Django 4.2.6 on 2023-12-22 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metadata',
            name='spotify_old',
        ),
    ]