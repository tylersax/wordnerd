# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-28 04:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0015_auto_20170806_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbuser',
            name='subscribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 28, 4, 57, 49, 820265)),
        ),
        migrations.AlterField(
            model_name='wotd',
            name='day',
            field=models.DateField(default=datetime.datetime(2018, 1, 28, 4, 57, 49, 822127)),
        ),
    ]
