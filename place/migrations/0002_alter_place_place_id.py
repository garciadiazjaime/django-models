# Generated by Django 4.2.6 on 2023-11-15 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='place_id',
            field=models.CharField(max_length=240),
        ),
    ]
