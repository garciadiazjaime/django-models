# Generated by Django 4.2.6 on 2024-03-25 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_alter_musico_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musico',
            name='genres',
            field=models.ManyToManyField(blank=True, to='event.genre'),
        ),
    ]
