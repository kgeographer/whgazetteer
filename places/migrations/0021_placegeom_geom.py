# Generated by Django 2.2.20 on 2021-06-04 19:32

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0020_remove_place_collections'),
    ]

    operations = [
        migrations.AddField(
            model_name='placegeom',
            name='geom',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
