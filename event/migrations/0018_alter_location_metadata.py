# Generated by Django 4.2.6 on 2023-12-03 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0017_alter_metadata_wiki_page_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='metadata',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.metadata'),
        ),
    ]
