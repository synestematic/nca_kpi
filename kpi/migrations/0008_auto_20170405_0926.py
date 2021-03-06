# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 09:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi', '0007_auto_20170330_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats_ops',
            name='abandoned_soon_calls',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stats_ops',
            name='satisfied_calls',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stats_bc',
            name='date',
            field=models.DateField(default=datetime.date(2017, 4, 5), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stats_ops',
            name='date',
            field=models.DateField(default=datetime.date(2017, 4, 5), primary_key=True, serialize=False),
        ),
    ]
