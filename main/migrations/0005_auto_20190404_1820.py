# Generated by Django 2.1.7 on 2019-04-04 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190404_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='place_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='whg_id',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='note',
            field=models.CharField(blank=True, max_length=2044, null=True),
        ),
    ]
