# Generated by Django 3.0.2 on 2020-01-22 17:13

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observations_manager', '0008_auto_20200122_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='image_polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
    ]
