# Generated by Django 3.0.2 on 2020-01-21 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations_manager', '0005_auto_20200121_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='image_url',
            field=models.URLField(),
        ),
    ]