# Generated by Django 2.2.4 on 2019-10-23 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0007_auto_20191012_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='src_id',
            field=models.CharField(max_length=2044),
        ),
    ]
