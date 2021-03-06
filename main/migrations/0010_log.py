# Generated by Django 2.2.10 on 2020-03-10 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0018_auto_20200310_1437'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0009_auto_20190406_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('user', 'User'), ('dataset', 'Dataset')], max_length=20)),
                ('logtype', models.CharField(choices=[('ds_create', 'Create dataset'), ('ds_update', 'Update dataset'), ('ds_delete', 'Delete dataset'), ('ds_recon', 'Reconciliation task'), ('area_create', 'Create dataset'), ('area_update', 'Update dataset'), ('area_delete', 'Delete dataset')], max_length=20)),
                ('note', models.CharField(blank=True, max_length=2044, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log', to='datasets.Dataset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'log',
                'managed': True,
            },
        ),
    ]
