# Generated by Django 4.2.6 on 2024-07-15 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_instagram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='buyUrl',
            field=models.URLField(blank=True, default='', max_length=420),
        ),
    ]
