# Generated by Django 2.2.20 on 2021-06-19 18:29

import collection.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0008_auto_20210608_0335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='tags',
            new_name='keywords',
        ),
        migrations.AddField(
            model_name='collection',
            name='contact',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='creator',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='webpage',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to=collection.models.coll_image_path),
        ),
    ]
