# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-15 17:13
from __future__ import unicode_literals

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('powersong', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='detailed_vectors',
            field=picklefield.fields.PickledObjectField(blank=True, editable=False, null=True),
        ),
    ]