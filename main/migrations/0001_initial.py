# Generated by Django 2.1.7 on 2019-04-04 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whg_id', models.IntegerField()),
                ('tag', models.CharField(choices=[('bad_link', 'Incorrect match/link'), ('bad_type', 'Incorrect place type'), ('typo', 'Typo'), ('other', 'Other')], default='other', max_length=20)),
                ('note', models.CharField(max_length=2044)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]