# Generated by Django 4.2.6 on 2024-01-26 19:26

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('profile', models.URLField()),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=240)),
                ('type', models.CharField(choices=[('ARTIST', 'ARTIST'), ('LOCATION', 'LOCATION')], max_length=24)),
                ('website', models.URLField(blank=True, default='')),
                ('image', models.URLField(blank=True, default='', max_length=420)),
                ('twitter', models.URLField(blank=True, default='')),
                ('facebook', models.URLField(blank=True, default='')),
                ('youtube', models.URLField(blank=True, default='')),
                ('instagram', models.URLField(blank=True, default='')),
                ('tiktok', models.URLField(blank=True, default='')),
                ('soundcloud', models.URLField(blank=True, default='')),
                ('appleMusic', models.URLField(blank=True, default='')),
                ('spotify', models.URLField(blank=True, default='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.IntegerField(default=0)),
                ('popularity', models.IntegerField(default=0)),
                ('url', models.URLField(blank=True, default='')),
                ('tries', models.PositiveSmallIntegerField(default=0)),
                ('image', models.URLField(blank=True, default='', max_length=240)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('genres', models.ManyToManyField(blank=True, to='event.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('address', models.TextField()),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('place_id', models.CharField(max_length=50)),
                ('website', models.URLField(default='')),
                ('meta_tries', models.PositiveSmallIntegerField(default=0)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name')),
                ('slug_venue', models.SlugField(max_length=240)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.metadata')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('description', models.TextField(blank=True, default='')),
                ('image', models.URLField()),
                ('url', models.URLField(max_length=420)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('provider', models.CharField(max_length=240)),
                ('venue', models.CharField(max_length=240)),
                ('address', models.CharField(blank=True, default='', max_length=240)),
                ('city', models.CharField(max_length=240)),
                ('rank', models.PositiveSmallIntegerField(default=0)),
                ('gmaps_tries', models.PositiveSmallIntegerField(default=0)),
                ('artist_tries', models.PositiveSmallIntegerField(default=0)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('artists', models.ManyToManyField(blank=True, to='event.artist')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.location')),
            ],
        ),
        migrations.AddField(
            model_name='artist',
            name='metadata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.metadata'),
        ),
        migrations.AddField(
            model_name='artist',
            name='spotify',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.spotify'),
        ),
    ]
