# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-20 05:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20160319_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postobject', models.CharField(max_length=100)),
                ('entry', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 20, 5, 6, 26, 857184)),
        ),
    ]
