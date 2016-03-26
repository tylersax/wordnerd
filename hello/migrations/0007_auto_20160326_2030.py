# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-26 20:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0006_auto_20160325_0206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('user', models.BigIntegerField()),
                ('state', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 26, 20, 30, 6, 646166)),
        ),
        migrations.AddField(
            model_name='conversation',
            name='topic',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hello.Topic'),
        ),
    ]
