# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-07 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powersong', '0004_auto_20171017_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listener',
            name='age',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='listener',
            name='country',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='listener',
            name='profile_image_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='listener',
            name='real_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='listener',
            name='scrobble_count',
            field=models.IntegerField(null=True),
        ),
    ]