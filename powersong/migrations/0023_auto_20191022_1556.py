# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-10-22 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersong', '0022_auto_20190319_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='strava_refresh_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='athlete',
            name='strava_token_expires_at',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='share_activity_link',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='share_activity_songs',
            field=models.BooleanField(default=True),
        ),
    ]
