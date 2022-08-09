# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-05 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersong', '0026_auto_20210404_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='acousticness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='bpm',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='danceability',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='energy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='instrumentalness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='key',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='liveness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='loudness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='mode',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='speechiness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='time_signature',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='valence',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
