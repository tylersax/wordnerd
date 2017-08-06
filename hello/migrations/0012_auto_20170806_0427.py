# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-06 04:27
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0011_auto_20160918_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggedMessage',
            fields=[
                ('mid', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('timestamp_logged', models.DateTimeField()),
                ('timestamp_sent', models.DateTimeField()),
                ('message_type', models.CharField(choices=[(b'sent', b'sent'), (b'recieved', b'recieved'), (b'read', b'read'), (b'delivered', b'delivered'), (b'null', b'null')], default=b'null', max_length=20)),
                ('api_id', models.BigIntegerField()),
                ('payload', models.CharField(blank=True, max_length=50)),
                ('text', models.TextField(blank=True)),
                ('attachment_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, size=8)),
                ('extra', models.TextField(blank=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='hello.FBUser')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='hello.FBUser')),
            ],
        ),
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 6, 4, 27, 10, 71112)),
        ),
        migrations.AlterField(
            model_name='wotd',
            name='day',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 4, 27, 10, 72958)),
        ),
    ]
