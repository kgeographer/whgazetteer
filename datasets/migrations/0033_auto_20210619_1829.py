# Generated by Django 2.2.20 on 2021-06-19 18:29

import datasets.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0032_auto_20210608_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='contributors',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='source',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to=datasets.models.ds_image_path),
        ),
    ]
