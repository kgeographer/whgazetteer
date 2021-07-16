# Generated by Django 2.2.20 on 2021-06-18 16:52

import collection.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datasets', '0027_auto_20210424_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2044)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('image_file', models.FileField(upload_to=collection.models.user_directory_path)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('public', models.BooleanField(default=False)),
                ('featured', models.IntegerField(blank=True, null=True)),
                ('datasets', models.ManyToManyField(to='datasets.Dataset')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collections',
            },
        ),
    ]
