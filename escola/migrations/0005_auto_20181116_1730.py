# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-16 17:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0004_auto_20180428_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 11, 16, 17, 30, 38, 755610)),
        ),
        migrations.AlterField(
            model_name='historicalconfiguracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 11, 16, 17, 30, 38, 755610)),
        ),
    ]