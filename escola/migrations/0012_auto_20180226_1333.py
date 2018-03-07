# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-26 13:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0011_auto_20180224_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracoes',
            name='validade_parecer',
        ),
        migrations.RemoveField(
            model_name='historicalconfiguracoes',
            name='validade_parecer',
        ),
        migrations.AddField(
            model_name='configuracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 2, 26, 13, 33, 3, 309256)),
        ),
        migrations.AddField(
            model_name='historicalconfiguracoes',
            name='data_validade_parecer',
            field=models.DateField(default=datetime.datetime(2018, 2, 26, 13, 33, 3, 309256)),
        ),
    ]