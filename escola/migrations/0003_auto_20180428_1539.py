# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 15:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0002_auto_20180428_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 4, 28, 15, 39, 5, 735286)),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 4, 28, 15, 39, 5, 735286)),
        ),
    ]
