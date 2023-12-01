# Generated by Django 4.2.6 on 2023-12-01 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_alter_event_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('image', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('youtube', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('tiktok', models.URLField(blank=True, null=True)),
                ('soundcloud', models.URLField(blank=True, null=True)),
                ('spotify', models.URLField(blank=True, null=True)),
                ('appleMusic', models.URLField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('title', models.CharField(blank=True, max_length=240, null=True)),
                ('description', models.CharField(blank=True, max_length=240, null=True)),
                ('type', models.CharField(blank=True, max_length=240, null=True)),
                ('wiki_page_id', models.CharField(blank=True, max_length=20, null=True)),
                ('wiki_title', models.CharField(blank=True, max_length=240, null=True)),
                ('wiki_description', models.CharField(blank=True, max_length=240, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='name',
        ),
        migrations.AddField(
            model_name='event',
            name='artist',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='event.artist'),
            preserve_default=False,
        ),
    ]