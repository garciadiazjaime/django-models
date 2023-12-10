# Generated by Django 4.2.6 on 2023-12-10 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_artist_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='slug_venue',
            field=models.SlugField(default='', max_length=240),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.location'),
        ),
    ]
