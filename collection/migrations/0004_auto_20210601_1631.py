# Generated by Django 2.2.20 on 2021-06-01 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_auto_20210529_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectionplace',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='collectionplace',
            name='place',
        ),
        migrations.DeleteModel(
            name='CollectionDataset',
        ),
        migrations.DeleteModel(
            name='CollectionPlace',
        ),
    ]
